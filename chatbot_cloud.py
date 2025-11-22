#!/usr/bin/env python3
"""
Cloud-Ready Chatbot with Function Calling
Deployed on Google Cloud Run with external agent discovery
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ADK imports for A2A agent calls
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions import InMemorySessionService

load_dotenv()

app = FastAPI(
    title="Stock Analysis Chatbot - Cloud Function Calling",
    description="Gemini API function calling with A2A agents on Google Cloud",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Internal agent URLs (from Cloud Run env vars or defaults)
INTERNAL_AGENTS = {
    "fundamental": os.getenv("FUNDAMENTAL_AGENT_URL", "http://localhost:8001"),
    "technical": os.getenv("TECHNICAL_AGENT_URL", "http://localhost:8002"),
    "sentiment": os.getenv("SENTIMENT_AGENT_URL", "http://localhost:8003"),
    "macro": os.getenv("MACRO_AGENT_URL", "http://localhost:8004"),
    "regulatory": os.getenv("REGULATORY_AGENT_URL", "http://localhost:8005"),
    "predictor": os.getenv("PREDICTOR_AGENT_URL", "http://localhost:8006"),
}

# External agent registry (can be populated from agent marketplace/discovery service)
EXTERNAL_AGENTS = {}

# Agent Registry URL (for discovering external agents)
AGENT_REGISTRY_URL = os.getenv("AGENT_REGISTRY_URL", "http://localhost:9000")


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    function_calls: List[Dict[str, Any]]
    session_id: str


def discover_external_agents():
    """Discover external agents from registry."""
    global EXTERNAL_AGENTS
    try:
        response = requests.get(f"{AGENT_REGISTRY_URL}/agents", timeout=5)
        if response.status_code == 200:
            registry_agents = response.json()
            for agent in registry_agents.get("agents", []):
                agent_id = agent.get("id")
                agent_card_url = agent.get("agent_card_url")
                if agent_id and agent_card_url:
                    EXTERNAL_AGENTS[agent_id] = {
                        "name": agent.get("name", agent_id),
                        "description": agent.get("description", ""),
                        "agent_card_url": agent_card_url,
                        "category": agent.get("category", "general")
                    }
            print(f"✅ Discovered {len(EXTERNAL_AGENTS)} external agents")
    except Exception as e:
        print(f"⚠️  Could not connect to agent registry: {e}")


def call_a2a_agent(agent_url: str, ticker: str, query: str = None) -> str:
    """Call an A2A agent."""
    try:
        card_url = f"{agent_url}/.well-known/agent-card.json"
        agent = RemoteA2aAgent(name="agent", agent_card=card_url)
        
        session_service = InMemorySessionService()
        session_id = f"{ticker}_{int(datetime.now().timestamp())}"
        session = session_service.create_session(session_id=session_id)
        
        context = InvocationContext(
            session_service=session_service,
            invocation_id=f"inv_{int(datetime.now().timestamp())}",
            agent=agent,
            session=session
        )
        
        prompt = query or f"Analyze {ticker}"
        
        async def run_agent():
            full_response = ""
            async for event in agent.run_async(context):
                if hasattr(event, 'content'):
                    full_response += str(event.content)
                elif hasattr(event, 'text'):
                    full_response += event.text
            return full_response
        
        return asyncio.run(run_agent())
    except Exception as e:
        return json.dumps({"error": str(e)})


def call_external_agent(agent_id: str, prompt: str) -> str:
    """Call an external A2A agent."""
    if agent_id not in EXTERNAL_AGENTS:
        return json.dumps({"error": f"Agent {agent_id} not found"})
    
    agent_info = EXTERNAL_AGENTS[agent_id]
    card_url = agent_info["agent_card_url"]
    
    try:
        agent = RemoteA2aAgent(name=agent_id, agent_card=card_url)
        session_service = InMemorySessionService()
        session_id = f"ext_{int(datetime.now().timestamp())}"
        session = session_service.create_session(session_id=session_id)
        
        context = InvocationContext(
            session_service=session_service,
            invocation_id=f"inv_{int(datetime.now().timestamp())}",
            agent=agent,
            session=session
        )
        
        async def run_agent():
            full_response = ""
            async for event in agent.run_async(context):
                if hasattr(event, 'content'):
                    full_response += str(event.content)
                elif hasattr(event, 'text'):
                    full_response += event.text
            return full_response
        
        return asyncio.run(run_agent())
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_function_declarations():
    """Get function declarations including external agents."""
    functions = [
        {
            "name": "analyze_fundamentals",
            "description": "Analyze company fundamentals including financial metrics, valuation ratios.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "query": {"type": "string", "description": "Optional specific question"}
                },
                "required": ["ticker"]
            }
        },
        {
            "name": "analyze_technical",
            "description": "Perform technical analysis including price trends, RSI, MACD.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "query": {"type": "string", "description": "Optional specific question"}
                },
                "required": ["ticker"]
            }
        },
        {
            "name": "analyze_sentiment",
            "description": "Analyze news sentiment and key events affecting the stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "query": {"type": "string", "description": "Optional specific question"}
                },
                "required": ["ticker"]
            }
        },
        {
            "name": "analyze_macro",
            "description": "Analyze macroeconomic conditions including GDP, inflation, Fed rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "query": {"type": "string", "description": "Optional specific question"}
                },
                "required": ["ticker"]
            }
        },
        {
            "name": "analyze_regulatory",
            "description": "Check regulatory risks, SEC filings, compliance issues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "query": {"type": "string", "description": "Optional specific question"}
                },
                "required": ["ticker"]
            }
        },
        {
            "name": "get_full_analysis",
            "description": "Get complete stock analysis using all specialist agents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["ticker"]
            }
        }
    ]
    
    # Add external agent functions
    for agent_id, agent_info in EXTERNAL_AGENTS.items():
        functions.append({
            "name": f"call_external_{agent_id}",
            "description": f"{agent_info['description']} - External agent: {agent_info['name']}",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Query for the external agent"}
                },
                "required": ["prompt"]
            }
        })
    
    return functions


FUNCTION_IMPLEMENTATIONS = {
    "analyze_fundamentals": lambda args: call_a2a_agent(INTERNAL_AGENTS["fundamental"], args["ticker"], args.get("query")),
    "analyze_technical": lambda args: call_a2a_agent(INTERNAL_AGENTS["technical"], args["ticker"], args.get("query")),
    "analyze_sentiment": lambda args: call_a2a_agent(INTERNAL_AGENTS["sentiment"], args["ticker"], args.get("query")),
    "analyze_macro": lambda args: call_a2a_agent(INTERNAL_AGENTS["macro"], args["ticker"], args.get("query")),
    "analyze_regulatory": lambda args: call_a2a_agent(INTERNAL_AGENTS["regulatory"], args["ticker"], args.get("query")),
    "get_full_analysis": lambda args: get_full_analysis(args["ticker"])
}


def get_full_analysis(ticker: str) -> str:
    """Get comprehensive analysis from all agents."""
    results = {}
    for agent_type in ["fundamental", "technical", "sentiment", "macro", "regulatory"]:
        try:
            result = call_a2a_agent(INTERNAL_AGENTS[agent_type], ticker)
            results[agent_type] = result
        except Exception as e:
            results[agent_type] = {"error": str(e)}
    return json.dumps(results, indent=2)


def setup_external_agent_functions():
    """Setup function implementations for external agents."""
    for agent_id in EXTERNAL_AGENTS.keys():
        def make_impl(aid):
            return lambda args: call_external_agent(aid, args["prompt"])
        FUNCTION_IMPLEMENTATIONS[f"call_external_{agent_id}"] = make_impl(agent_id)


def chat_with_function_calling(user_message: str) -> tuple[str, List[Dict]]:
    """Chat with Gemini using function calling."""
    functions = get_function_declarations()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GOOGLE_API_KEY}"
    
    function_calls_made = []
    contents = [{"role": "user", "parts": [{"text": user_message}]}]
    max_iterations = 5
    
    for iteration in range(max_iterations):
        payload = {
            "contents": contents,
            "tools": [{"function_declarations": functions}],
            "system_instruction": "You are a helpful stock analysis assistant. Use internal agents for stock analysis. Use external agents for additional intelligence when appropriate."
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "candidates" not in result or not result["candidates"]:
            break
        
        candidate = result["candidates"][0]
        if "content" not in candidate or "parts" not in candidate["content"]:
            break
        
        parts = candidate["content"]["parts"]
        function_call = None
        
        for part in parts:
            if "functionCall" in part:
                function_call = part["functionCall"]
                break
        
        if not function_call:
            break
        
        function_name = function_call.get("name", "")
        function_args = function_call.get("args", {})
        
        function_calls_made.append({"name": function_name, "args": function_args})
        
        # Execute function
        if function_name in FUNCTION_IMPLEMENTATIONS:
            function_result = FUNCTION_IMPLEMENTATIONS[function_name](function_args)
        else:
            function_result = json.dumps({"error": f"Unknown function: {function_name}"})
        
        contents.append({"role": "model", "parts": [{"functionCall": function_call}]})
        contents.append({
            "role": "function",
            "parts": [{"functionResponse": {"name": function_name, "response": function_result}}]
        })
    
    # Get final response
    if function_calls_made:
        payload = {"contents": contents}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
    
    if "candidates" in result and result["candidates"]:
        parts = result["candidates"][0]["content"]["parts"]
        response_text = "".join([part.get("text", "") for part in parts])
    else:
        response_text = f"I analyzed your request and called {len(function_calls_made)} function(s)."
    
    return response_text, function_calls_made


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Stock Analysis Chatbot - Function Calling Demo",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "external_agents": "/agents/external",
            "discover_agents": "/agents/discover (POST)",
            "docs": "/docs"
        },
        "external_agents_count": len(EXTERNAL_AGENTS)
    }


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy", "external_agents": len(EXTERNAL_AGENTS)}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with function calling."""
    try:
        response_text, function_calls = chat_with_function_calling(request.message)
        session_id = request.session_id or f"session_{int(datetime.now().timestamp())}"
        return ChatResponse(
            response=response_text,
            function_calls=function_calls,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents/external")
async def list_external_agents():
    """List discovered external agents."""
    return {"agents": list(EXTERNAL_AGENTS.values())}


@app.post("/agents/discover")
async def discover_agents():
    """Trigger agent discovery."""
    discover_external_agents()
    return {"status": "discovered", "count": len(EXTERNAL_AGENTS)}


# Discover agents on startup
@app.on_event("startup")
async def startup():
    """Discover external agents on startup."""
    discover_external_agents()
    setup_external_agent_functions()


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

