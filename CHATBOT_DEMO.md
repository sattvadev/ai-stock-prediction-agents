# 🤖 Function Calling Chatbot Demo

**Assessment Criteria: Function Calling Demonstration**

This chatbot demonstrates **Gemini API function calling** integrated with your A2A agents. Perfect for showing function calling in action!

## ✨ What It Demonstrates

- ✅ **Function Calling** - Gemini decides which functions to call based on user queries
- ✅ **A2A Integration** - Functions call your existing A2A agents
- ✅ **Multi-Agent Orchestration** - Seamlessly routes to specialist agents
- ✅ **Google Ecosystem** - Built with Google Gemini API + Google ADK
- ✅ **Visual Demo** - Clean Streamlit UI showing function calls in real-time

## 🚀 Quick Start

### 1. Start Your A2A Agents

```bash
bash scripts/start_all_agents.sh
```

### 2. Install Dependencies

```bash
pip install -r requirements_chatbot.txt
```

### 3. Set API Key

```bash
export GOOGLE_API_KEY=your_key_here
```

### 4. Start Chatbot

```bash
bash scripts/start_chatbot.sh
```

Or directly:

```bash
streamlit run chatbot_function_calling.py
```

### 5. Open Browser

Navigate to: `http://localhost:8501`

## 💬 Example Queries

Try these to see function calling in action:

```
Analyze AAPL fundamentals
What's the technical outlook for GOOGL?
Get full analysis of MSFT
Check sentiment for TSLA
What are the macro conditions?
```

## 🔧 How Function Calling Works

1. **User asks a question** → "Analyze AAPL fundamentals"

2. **Gemini analyzes the query** → Decides to call `analyze_fundamentals(ticker="AAPL")`

3. **Function executes** → Calls your A2A fundamental agent via `RemoteA2aAgent`

4. **Result returned** → Gemini receives the analysis and formulates a response

5. **User sees** → Both the response AND the function calls made (expandable section)

## 📋 Available Functions

The chatbot exposes 6 functions to Gemini:

| Function | Purpose | Calls Agent |
|----------|---------|-------------|
| `analyze_fundamentals(ticker)` | Financial metrics, valuation | Fundamental Analyst |
| `analyze_technical(ticker)` | Price trends, indicators | Technical Analyst |
| `analyze_sentiment(ticker)` | News sentiment, events | Sentiment Analyst |
| `analyze_macro(ticker)` | Economic conditions | Macro Analyst |
| `analyze_regulatory(ticker)` | SEC filings, compliance | Regulatory Analyst |
| `get_full_analysis(ticker)` | Complete analysis | All agents + Predictor |

## 🎯 Assessment Criteria Coverage

### ✅ Function Calling
- **Clear demonstration**: Function calls shown in expandable UI sections
- **Multiple functions**: 6 different functions available
- **Intelligent routing**: Gemini decides which functions to call
- **Real execution**: Functions actually call your A2A agents

### ✅ Google Ecosystem
- **Gemini API**: Using `google-generativeai` library
- **ADK Integration**: Using `RemoteA2aAgent` from Google ADK
- **A2A Protocol**: Your agents exposed via A2A cards

### ✅ Visual Demo
- **Streamlit UI**: Clean, professional interface
- **Function call visibility**: Shows exactly what functions were called
- **Agent status**: Real-time status of all A2A agents
- **Chat history**: Full conversation context

## 🏗️ Architecture

```
User Query
    ↓
Gemini API (with function declarations)
    ↓
Function Call Decision
    ↓
Function Implementation
    ↓
RemoteA2aAgent → A2A Agent (Port 8001-8006)
    ↓
Response → Gemini → User
```

## 📸 What You'll See

1. **Chat Interface** - Clean conversation UI
2. **Function Calls Section** - Expandable JSON showing:
   - Function name
   - Arguments passed
   - Execution status
3. **Agent Status** - Sidebar showing which agents are online
4. **Example Queries** - Quick suggestions

## 🎓 For Assessment

This demo clearly shows:

1. **Function calling implementation** - Real code using Gemini API
2. **Function declarations** - Proper schema definitions
3. **Function execution** - Actual calls to A2A agents
4. **Integration** - Google ADK + A2A + Gemini
5. **User experience** - Professional chatbot interface

## 🔍 Code Highlights

**Function Declarations:**
```python
types.FunctionDeclaration(
    name="analyze_fundamentals",
    description="Analyze company fundamentals...",
    parameters=types.Schema(...)
)
```

**Function Execution:**
```python
function_result = FUNCTION_IMPLEMENTATIONS[function_name](function_args)
```

**A2A Agent Call:**
```python
agent = RemoteA2aAgent(name="fundamental_agent", agent_card=card_url)
response = await agent.run_async(context)
```

## 🚀 Deployment Options

### Local Demo
- Run `streamlit run chatbot_function_calling.py`
- Perfect for assessment demo

### Google Cloud Run
- Containerize with Docker
- Deploy to Cloud Run
- Access via HTTPS

### Vertex AI Integration
- Can be integrated with Vertex AI Agent Builder
- Use as a custom tool

## 📝 Notes

- **Requires agents running**: All 6 A2A agents must be running
- **API key needed**: Set `GOOGLE_API_KEY` environment variable
- **Port 8501**: Default Streamlit port (changeable)

## 🎉 Perfect For

- ✅ Assessment demonstration
- ✅ Showing function calling in action
- ✅ Google ecosystem integration showcase
- ✅ A2A protocol demonstration
- ✅ Multi-agent system demo

---

**Built with:** Google Gemini API • Google ADK • A2A Protocol • Streamlit

