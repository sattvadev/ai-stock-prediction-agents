# 🤖 AI Stock Prediction System - Kaggle Capstone Submission

**Authors:** Nishant Pithia & Vagge Sneha  
**Course:** Kaggle 5-Day Agents Intensive

## 🎯 Project Overview

A production-ready multi-agent stock prediction system using Google's Agent Development Kit (ADK) and A2A Protocol v0.3.0. The system deploys 6 specialized AI agents that work in parallel to analyze stocks from different dimensions, then synthesize their insights into actionable investment recommendations.

### Key Highlights

✅ **Full A2A Protocol Implementation** - Complete JSONRPC-based agent-to-agent communication  
✅ **6 Specialist Agents** - Fundamental, Technical, Sentiment, Macro, Regulatory, and Predictor  
✅ **Real Financial APIs** - Polygon.io, FRED, NewsAPI, SEC Edgar  
✅ **Production Deployment** - Complete Google Cloud Platform deployment with auto-scaling  
✅ **Beautiful Agentic UI** - Real-time workflow visualization showing agents working in parallel  
✅ **Comprehensive Jupyter Notebook** - Full demonstration with live analysis

## 🏗️ Architecture

```
Strategist Orchestrator (Coordinator Pattern)
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

### Agent Responsibilities

| Agent | Data Source | Analysis Focus |
|-------|-------------|----------------|
| **Fundamental** | Polygon + SEC | Financial metrics, valuation ratios, balance sheet |
| **Technical** | Polygon | Price trends, indicators (RSI, MACD, MA) |
| **Sentiment** | NewsAPI + Polygon | News analysis, market sentiment, events |
| **Macro** | FRED | Economic indicators, Fed policy, GDP, inflation |
| **Regulatory** | SEC Edgar | Filings, compliance, legal risks |
| **Predictor** | All agents | Synthesis, final recommendation |

## 🚀 Running the System

### Option 1: Cloud Deployment (Recommended)

Deploy to Google Cloud Platform in 15 minutes:

```bash
# Deploy backend
./deploy/deploy.sh

# Deploy UI
./deploy/deploy-vertex-ui.sh

# Test
./deploy/test-deployment.sh
```

See **[VERTEX_AI_DEPLOYMENT.md](VERTEX_AI_DEPLOYMENT.md)** for complete instructions.

### Option 2: Local Development

```bash
# Start all agents
bash scripts/start_all_agents.sh

# Start frontend
cd frontend && npm install && npm run dev &

# Start backend API
python frontend_api.py

# Open http://localhost:3001
```

### Option 3: Jupyter Notebook

```bash
jupyter notebook
# Open: notebooks/kaggle_submission_complete.ipynb
```

## 📊 Demonstration

### Sample Analysis Output

```
🔍 Analyzing AAPL for next_quarter...
============================================================
📊 Phase 1: Specialist Agent Analysis
------------------------------------------------------------
   🔄 Calling Fundamental Analyst...
   🔄 Calling Technical Analyst...
   🔄 Calling Sentiment Analyst...
   🔄 Calling Macro Analyst...
   🔄 Calling Regulatory Analyst...

   🟢 Fundamental: Signal +0.40, Confidence 78%
   🟢 Technical: Signal +0.24, Confidence 57%
   🟢 Sentiment: Signal +0.47, Confidence 65%
   🟡 Macro: Signal +0.30, Confidence 72%
   🟡 Regulatory: Signal +0.00, Confidence 58%

🎯 Phase 2: Final Prediction Synthesis
------------------------------------------------------------
   📊 Final Recommendation: BUY
   💪 Confidence: 66.0%
   ⚡ Risk Level: MEDIUM
   ⏱️  Completed in 4.18s
```

## 🎓 Gen AI Capabilities Demonstrated

This project showcases **15+ advanced capabilities** from the course:

### Core A2A Implementation
1. **Agent-to-Agent Communication** - Full A2A Protocol v0.3.0 with JSONRPC
2. **Agent Cards** - `.well-known/agent-card.json` for discovery
3. **Multi-Agent Orchestration** - Coordinator pattern with parallel execution
4. **Session Management** - Context handling across agent conversations

### Advanced Features
5. **Custom Tools** - 5 real API integrations (Polygon, FRED, NewsAPI, SEC, Gemini)
6. **Structured Output** - Pydantic schemas for type-safe responses
7. **Streaming Responses** - Real-time progress updates in UI
8. **Error Handling** - Graceful degradation and fallbacks
9. **RAG Pattern** - Knowledge bases in system prompts
10. **Long Context** - Leveraging Gemini's 2M token window

### Production Features
11. **Deployment** - Complete Google Cloud deployment
12. **Monitoring** - Cloud Logging and Error Reporting
13. **Security** - Secret Manager for API keys
14. **Scaling** - Auto-scaling 0-10 instances per service
15. **UI/UX** - Real-time agentic workflow visualization

## 🎨 Agentic UI Features

Our deployed UI includes:

- **Real-Time Agent Workflow** - Watch all 6 agents work in parallel
- **Execution Timeline** - Timestamped events showing exact progress
- **Signal Visualization** - Color-coded bars (red/yellow/green)
- **Confidence Gauges** - Per-agent certainty levels
- **Beautiful Dark Theme** - Glassmorphism effects and smooth animations
- **Mobile Responsive** - Works on any device
- **PWA-Ready** - Install as app on mobile

## 📁 Project Structure

```
Agent Capstone/
├── agents/                  # A2A agent servers
│   ├── fundamental_analyst_server.py
│   ├── technical_analyst_server.py
│   ├── news_sentiment_analyst_server.py
│   ├── macro_analyst_server.py
│   ├── regulatory_analyst_server.py
│   ├── predictor_agent_server.py
│   ├── kaggle_orchestrator.py
│   └── cloud_orchestrator.py
├── tools/                   # Data fetching tools
│   ├── polygon_fetcher.py
│   ├── fred_fetcher.py
│   ├── news_fetcher.py
│   └── sec_edgar_fetcher.py
├── frontend/               # Next.js web interface
├── notebooks/              # Jupyter notebooks
│   └── kaggle_submission_complete.ipynb
├── deploy/                 # GCP deployment files
├── main.py                 # CLI entry point
├── frontend_api.py         # FastAPI backend
└── requirements.txt        # Dependencies
```

## 💰 Cost & Performance

### Performance
- **Analysis Time**: 4-8 seconds
- **Agent Startup**: < 2 seconds
- **Parallel Execution**: All 5 specialist agents run simultaneously
- **Accuracy**: Confidence scores 60-75% (realistic, not overfit)

### Cloud Deployment Costs
- **Free Tier**: $0-5/month (2M requests)
- **Light Use**: $9-14/month (< 100 analyses/day)
- **Medium Use**: $20-29/month (< 1000 analyses/day)
- **Auto-Scaling**: Scale to zero when idle

## 🔐 Security & Production Features

✅ **API Key Management** - Secret Manager (never in code)  
✅ **HTTPS Everywhere** - Google-managed certificates  
✅ **Auto-Scaling** - 0-10 instances per service  
✅ **Monitoring** - Cloud Logging & Error Reporting  
✅ **Health Checks** - Automatic unhealthy instance replacement  
✅ **Zero-Downtime Deploys** - Gradual traffic shifting  

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[README.md](README.md)** | Project overview and local setup |
| **[VERTEX_AI_DEPLOYMENT.md](VERTEX_AI_DEPLOYMENT.md)** | Complete cloud deployment guide |
| **[ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md)** | System architecture details |
| **[API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)** | API key setup instructions |
| **deploy/** | Cloud deployment files and guides |

## 🧪 Testing

```bash
# Verify setup
python verify_setup.py

# Test agents
bash scripts/start_all_agents.sh
curl http://localhost:8001/.well-known/agent-card.json

# Run full analysis
python main.py --ticker AAPL

# Test cloud deployment
./deploy/test-deployment.sh
```

## 🎉 Key Achievements

1. ✅ **Production-Grade System** - Fully deployed on Google Cloud
2. ✅ **Complete A2A Protocol** - Full implementation with JSONRPC
3. ✅ **Real Data Sources** - 4 external APIs with live data
4. ✅ **Beautiful UI** - Real-time agentic workflow visualization
5. ✅ **Comprehensive Documentation** - 7+ guides covering all aspects
6. ✅ **Jupyter Notebook** - Complete demonstration with explanations
7. ✅ **Fast Performance** - 4-8 second analysis time
8. ✅ **Auto-Scaling** - Production-ready infrastructure

## 🔗 Links

- **Cloud Deployment Guide**: [VERTEX_AI_DEPLOYMENT.md](VERTEX_AI_DEPLOYMENT.md)
- **Jupyter Notebook**: [notebooks/kaggle_submission_complete.ipynb](notebooks/kaggle_submission_complete.ipynb)
- **Architecture**: [ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md)
- **GitHub**: (Add your repo URL)

## 🙏 Acknowledgments

- **Google ADK Team** - For the Agent Development Kit
- **Kaggle** - For the 5-Day Agents Intensive course
- **Polygon.io** - For comprehensive market data
- **FRED** - For economic indicators
- **NewsAPI** - For sentiment analysis data

---

**Built with ❤️ using Google ADK, Vertex AI, Gemini, and the A2A Protocol**

**For evaluation, please see:**
1. This document for overview
2. `notebooks/kaggle_submission_complete.ipynb` for live demonstration
3. `VERTEX_AI_DEPLOYMENT.md` for production deployment
4. `ARCHITECTURE_SUMMARY.md` for technical details

