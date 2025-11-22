# AI Stock Prediction System: Multi-Agent A2A Architecture

## Production-Ready Financial Analysis Using 6 Specialized AI Agents

---

## Problem Statement

Stock market analysis requires synthesizing information from multiple dimensions: financial fundamentals, technical indicators, market sentiment, macroeconomic conditions, and regulatory factors. Traditional approaches either rely on single models that lack domain expertise or require manual analysis that is time-consuming and error-prone. Investors need a system that can:

- Analyze stocks comprehensively across all critical dimensions simultaneously
- Provide explainable, transparent decisions with clear reasoning
- Deliver fast, actionable insights (under 10 seconds)
- Scale to handle multiple analyses without manual intervention
- Integrate real-time data from authoritative financial sources

This problem is particularly relevant for enterprise workflows where data analysis automation can significantly improve decision-making speed and accuracy.

---

## Solution

We built a **production-ready multi-agent stock prediction system** that addresses these challenges through specialized AI agents working in concert. The system uses Google's Agent Development Kit (ADK) and the Agent-to-Agent (A2A) Protocol v0.3.0 to coordinate 6 specialized agents, each an expert in their domain:

1. **Fundamental Analyst** - Analyzes financial metrics, valuation ratios, and balance sheets
2. **Technical Analyst** - Evaluates price trends, momentum, and technical indicators (RSI, MACD)
3. **Sentiment Analyst** - Processes news articles and market sentiment
4. **Macro Analyst** - Assesses economic indicators, Fed policy, and GDP trends
5. **Regulatory Analyst** - Reviews SEC filings, compliance issues, and legal risks
6. **Predictor Agent** - Synthesizes all agent insights into final recommendations

Each agent operates independently as a microservice, analyzing stocks in parallel. A central orchestrator coordinates the workflow using the A2A Protocol, ensuring seamless communication while maintaining agent autonomy. The system integrates real-time data from 4 financial APIs (Polygon.io, FRED, NewsAPI, SEC Edgar) and delivers comprehensive analysis in 4-10 seconds with 65-70% confidence scores.

**Why Agents?** Unlike single-model approaches, specialized agents allow each component to focus on its domain expertise. This parallel architecture is faster, more accurate, and provides complete transparency—every agent's decision is visible and explainable. The A2A Protocol enables agents to communicate seamlessly while remaining independently scalable and deployable.

---

## Architecture

The system follows a **Coordinator Pattern** (Day 1b) with three main layers:

### Orchestration Layer
The **Strategist Orchestrator** manages the entire workflow:
- Receives user requests (ticker symbol, prediction horizon)
- Decomposes tasks for specialized agents
- Coordinates parallel execution via A2A Protocol
- Synthesizes final predictions with weighted signals

### Specialized Agent Layer
Six A2A-compliant agents run as independent microservices:
- Each agent exposes an agent card at `/.well-known/agent-card.json`
- Communication via JSONRPC transport (A2A Protocol v0.3.0)
- Agents run on ports 8001-8006, independently scalable
- Each agent uses Gemini models with domain-specific prompts

### Data Integration Layer
Custom tools wrap real financial APIs:
- **Polygon.io** - Stock prices, fundamentals, technicals, news
- **FRED API** - Macroeconomic indicators (GDP, inflation, Fed rates)
- **SEC Edgar** - Regulatory filings (10-K, 10-Q, 8-K)
- **NewsAPI** - Market news and sentiment data

```
Strategist Orchestrator (Coordinator)
         ↓ A2A Protocol (JSONRPC)
    ┌────┴───┬────────┬────────┬────────┬────────┐
    │        │        │        │        │        │
Fundamental Technical Sentiment  Macro  Regulatory Predictor
  Agent      Agent     Agent   Agent     Agent    Agent
    │        │        │        │        │        │
    └────────┴────────┴────────┴────────┴────────┘
              External Data Sources
    Polygon.io, FRED, NewsAPI, SEC Edgar, Gemini
```

**Deployment**: The system is fully deployed on Google Cloud Run with auto-scaling (0-10 instances), HTTPS, Cloud Logging, and Secret Manager for API keys. The architecture supports both local development and production cloud deployment.

---

## Key Features Demonstrated

This project demonstrates **7 advanced concepts** from the Kaggle 5-Day Agents course:

### 1. Multi-Agent System (Coordinator Pattern)
The system uses a coordinator orchestrator that manages 6 specialized agents. Each agent is an LLM-powered expert in their domain, and agents execute in parallel for speed. The coordinator synthesizes their outputs into a final recommendation, demonstrating hierarchical task decomposition.

**Implementation**: `agents/kaggle_orchestrator.py` coordinates all agents using parallel execution with `asyncio` and `aiohttp` for concurrent API calls.

### 2. A2A Protocol (Full v0.3.0 Implementation)
Complete Agent-to-Agent communication using A2A Protocol v0.3.0 with JSONRPC transport. Each agent exposes an agent card for discovery and uses standardized JSONRPC methods for communication.

**Implementation**: All 6 agents (`agents/*_server.py`) implement A2A Protocol with `.well-known/agent-card.json` endpoints. The orchestrator uses `RemoteA2aAgent` to communicate with agents via JSONRPC.

### 3. Custom Tools (4 Real API Integrations)
The system integrates 4 real financial APIs through custom tools:
- `tools/polygon_fetcher.py` - Polygon.io API wrapper
- `tools/fred_fetcher.py` - FRED economic data
- `tools/sec_edgar_fetcher.py` - SEC filing parser
- `tools/news_fetcher.py` - Multi-source news aggregation

Each tool is properly documented with type hints, error handling, and structured return values that agents can use effectively.

### 4. Sessions & Memory
The orchestrator uses `InMemorySessionService` (Day 3a) to manage session state during analysis. Additionally, a memory bank stores historical predictions for comparison and learning.

**Implementation**: `agents/kaggle_orchestrator.py` creates sessions for each analysis and maintains a `memory_bank` dictionary storing ticker, analysis results, predictions, and timestamps for audit trails.

### 5. Observability (Logging, Tracing, Metrics)
Comprehensive logging throughout the system using Python's `logging` module. Cloud Logging integration for production deployment. Performance metrics tracked: execution time, confidence scores, agent signals, and API response times.

**Implementation**: All agents log their actions, and the orchestrator tracks timing metrics. Cloud Run deployment includes Cloud Logging for centralized observability.

### 6. Agent Evaluation
The system tracks evaluation metrics including:
- **Confidence Scores**: Per-agent confidence (55-85% range)
- **Execution Time**: 4-10 seconds average
- **Signal Differentiation**: Varies by stock (proves real analysis)
- **Agent Consensus**: Measures agreement between agents

**Implementation**: Metrics are calculated in `notebooks/kaggle_submission_complete.ipynb` and displayed in the frontend UI with performance scoring.

### 7. Agent Deployment
Full production deployment on Google Cloud Run with:
- Auto-scaling (0-10 instances per service)
- HTTPS with Google-managed certificates
- Secret Manager for API keys
- Cloud Logging and Error Reporting
- Health checks and zero-downtime deploys

**Implementation**: `deploy/` directory contains Cloud Build configurations, Dockerfiles, and deployment scripts. All 6 agents are containerized and deployed as separate Cloud Run services.

---

## Results & Value

The system delivers significant value for enterprise stock analysis workflows:

**Performance Metrics**:
- **Speed**: 4-10 second analysis time (vs. hours of manual research)
- **Accuracy**: 65-70% confidence scores (realistic, not overfit)
- **Scalability**: Parallel execution of 6 agents simultaneously
- **Transparency**: Every agent decision is explainable and traceable

**Real-World Impact**:
- **Time Savings**: Reduces analysis time from hours to seconds
- **Comprehensive Coverage**: Analyzes 5 critical dimensions simultaneously
- **Real-Time Data**: Integrates live data from 4 authoritative sources
- **Production-Ready**: Fully deployed and scalable on Google Cloud

**Cost Efficiency**:
- Cloud deployment: ~$0.02-0.05 per analysis (primarily Gemini API costs)
- Auto-scaling: Scales to zero when idle, pay only for usage
- Free tier available: $0-5/month for light usage

**Technical Achievements**:
- ✅ Complete A2A Protocol v0.3.0 implementation
- ✅ 6 specialized agents as independent microservices
- ✅ 4 real financial API integrations
- ✅ Production deployment with auto-scaling
- ✅ Modern Next.js frontend with real-time visualization
- ✅ Comprehensive Jupyter notebook demonstration

The system demonstrates that multi-agent architectures can deliver production-grade solutions for complex data analysis tasks, with complete transparency and explainability that single-model approaches cannot match.

---

## Code Repository

**GitHub**: https://github.com/sattvadev/ai-stock-prediction-agents

**Jupyter Notebook**: `notebooks/kaggle_submission_complete.ipynb` - Complete demonstration with live analysis

**Documentation**: See `README.md` for setup instructions and `ARCHITECTURE_SUMMARY.md` for technical details.

---

**Track**: Enterprise Agents  
**Built with**: Google ADK, Gemini 2.0 Flash, A2A Protocol v0.3.0, Google Cloud Run

