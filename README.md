# 🤖 AI Stock Prediction System - Multi-Agent A2A Architecture

> **Kaggle 5-Day Agents Capstone Project**  
> By **Nishant Pithia & Vagge Sneha**

Production-ready multi-agent stock prediction system using Google's Agent Development Kit (ADK) and A2A Protocol v0.3.0

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![ADK](https://img.shields.io/badge/Google-ADK-4285F4)](https://google.github.io/adk-docs/)
[![A2A Protocol](https://img.shields.io/badge/Protocol-A2A%20v0.3.0-green)](https://a2a-protocol.org/)

---

## 🎯 Project Overview

A **production-grade multi-agent system** that analyzes stocks using **7 specialized AI agents** communicating via the **Agent-to-Agent (A2A) protocol**. Each agent is an expert in their domain, and a central orchestrator synthesizes their insights into actionable predictions with investor-friendly explanations.

### 🏆 Key Features
- ✅ **Full A2A Protocol v0.3.0** with JSONRPC transport
- ✅ **4 Real Financial APIs** (Polygon.io, FRED, NewsAPI, SEC Edgar)
- ✅ **7 Specialized Agents** including Investor Advisor
- ✅ **4-10 second** end-to-end analysis time
- ✅ **Modern Next.js Frontend** with glassmorphic dark theme
- ✅ **Real-time news analysis** with sentiment breakdown
- ✅ **Complete transparency** - every agent response visible
- ✅ **Comprehensive Jupyter notebook** for Kaggle submission

### 💡 System Highlights
- **Specialized Expert Agents**: Fundamental, Technical, Sentiment, Macro, Regulatory, and Investor Advisor
- **Parallel Execution**: All agents analyze simultaneously
- **Real-Time Data**: Live API calls to financial data providers
- **Transparent AI**: Every agent decision is explainable
- **Professional UI**: Modern dark theme with detailed agent insights

---

## 🚀 Quick Start

### ☁️ Deploy to Google Cloud (Recommended)

Get your system live in production in 15 minutes:

```bash
# One-command deployment
./deploy/deploy.sh && ./deploy/deploy-vertex-ui.sh
```

See **[VERTEX_AI_DEPLOYMENT.md](VERTEX_AI_DEPLOYMENT.md)** for complete instructions.

**What you get:**
- ✅ Auto-scaling Cloud Run services
- ✅ Beautiful agentic UI with real-time workflow visualization
- ✅ Production monitoring and logging
- ✅ HTTPS everywhere
- ✅ Pay only for what you use (~$5-15/month)

### 💻 Run Locally

Prerequisites:
- Python 3.11 or higher
- Node.js 18+ (for frontend)
- API Keys (see below)

### Installation

```bash
# 1. Clone repository
git clone <your-repo-url>
cd "Agent Capstone"

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install
cd ..

# 5. Configure API keys
cp .env.example .env
# Edit .env and add your keys (see API Keys section below)
```

### Running the System

#### Option 1: Full System (Backend + Frontend)
```bash
# Start all services
bash scripts/start_full_system.sh

# Access the frontend at http://localhost:3001
# Backend API runs on http://localhost:8000
```

#### Option 2: CLI Only
```bash
# Start agent servers
bash scripts/start_all_agents.sh

# Run analysis
./venv/bin/python main.py --ticker AAPL

# Stop agents
bash scripts/stop_all_agents.sh
```

#### Option 3: Jupyter Notebook
```bash
# Launch Jupyter
jupyter notebook

# Open: notebooks/kaggle_submission_complete.ipynb
```

### Stopping the System
```bash
# Stop all services
bash scripts/stop_full_system.sh
```

---

## 🔑 API Keys Setup

### Required Keys

#### 1. **GOOGLE_API_KEY** (Required)
- **Purpose:** Powers all 7 AI agents using Gemini models
- **Get it:** https://aistudio.google.com/apikey
- **Cost:** Free tier available

#### 2. **POLYGON_API_KEY** (Required)
- **Purpose:** Stock prices, fundamentals, technicals, and news
- **Get it:** https://polygon.io/dashboard/api-keys
- **Cost:** Paid subscription (you already have this)

### Optional Keys

#### 3. **FRED_API_KEY** (Recommended)
- **Purpose:** Macro-economic data (GDP, inflation, Fed rates)
- **Get it:** https://fred.stlouisfed.org/docs/api/api_key.html
- **Cost:** FREE

#### 4. **NEWS_API_KEY** (Optional)
- **Purpose:** Alternative news source (Polygon already provides news)
- **Get it:** https://newsapi.org/register
- **Cost:** Free tier = 100 requests/day

### Configuration

Edit `.env` file:
```bash
GOOGLE_API_KEY=your_google_api_key_here
POLYGON_API_KEY=your_polygon_api_key_here
FRED_API_KEY=your_fred_api_key_here  # Optional but recommended
NEWS_API_KEY=your_news_api_key_here  # Optional
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│          Strategist Orchestrator            │
│        (Coordinator Pattern - Python)       │
└─────────────┬───────────────────────────────┘
              │ A2A Protocol (JSONRPC)
              ├──────────┬──────────┬──────────┬──────────┐
              ▼          ▼          ▼          ▼          ▼
   ┌─────────────┐  ┌──────────┐  ┌────────┐  ┌───────┐  ┌────────────┐
   │ Fundamental │  │Technical │  │Sentiment│  │ Macro │  │ Regulatory │
   │   Analyst   │  │ Analyst  │  │ Analyst │  │Analyst│  │  Analyst   │
   │  :8001      │  │  :8002   │  │  :8003  │  │ :8004 │  │   :8005    │
   └─────────────┘  └──────────┘  └────────┘  └───────┘  └────────────┘
         │                │            │           │            │
         ├────────────────┴────────────┴───────────┴────────────┤
         │                  Data Sources                         │
         ├─────────────┬─────────────┬──────────────┬───────────┤
         ▼             ▼             ▼              ▼           ▼
   Polygon.io      FRED API    NewsAPI.org    SEC Edgar   Google News
```

### Agent Responsibilities

| Agent | Port | Data Source | Purpose |
|-------|------|-------------|---------|
| **Fundamental Analyst** | 8001 | Polygon + SEC | Financial metrics, valuation |
| **Technical Analyst** | 8002 | Polygon | Price trends, indicators |
| **Sentiment Analyst** | 8003 | NewsAPI/Polygon | News analysis, market sentiment |
| **Macro Analyst** | 8004 | FRED | Economic indicators, Fed policy |
| **Regulatory Analyst** | 8005 | SEC Edgar | Compliance, legal risks |
| **Investor Advisor** | N/A | Gemini | Plain-English investment advice |
| **Orchestrator** | N/A | All agents | Coordination, final decision |

---

## 📊 Sample Analysis Output

```
🎯 Initializing Kaggle Competition Orchestrator...
📡 Verifying A2A agent deployment...
   ✅ Fundamental Agent (A2A v0.3.0)
   ✅ Technical Agent (A2A v0.3.0)
   ✅ Sentiment Agent (A2A v0.3.0)
   ✅ Macro Agent (A2A v0.3.0)
   ✅ Regulatory Agent (A2A v0.3.0)
✅ All 6 A2A agents verified and ready!

🔍 Analyzing AAPL for next_quarter...
======================================================================
📊 Phase 1: Parallel Multi-Agent Analysis
----------------------------------------------------------------------
   📊 Fundamental Analysis (Polygon API)...
   📈 Technical Analysis (Polygon API)...
   📰 Sentiment Analysis (News API + Polygon)...
   🌍 Macro-Economic Analysis (FRED API)...
   ⚖️  Regulatory Analysis (SEC Edgar API)...

   🟢 Fundamental: Signal +0.40, Confidence 78%
   🟢 Technical: Signal +0.24, Confidence 57%
   🟢 Sentiment: Signal +0.47, Confidence 65%
   🟡 Macro: Signal +0.30, Confidence 72%
   🟡 Regulatory: Signal +0.00, Confidence 58%

🎯 Phase 2: Final Prediction Synthesis
----------------------------------------------------------------------
   📊 Final Recommendation: BUY
   💪 Confidence: 66.0%
   ⚡ Risk Level: MEDIUM
   ⏱️  Completed in 4.18s
```

---

## 🖥️ Frontend Features

### Main Dashboard
- **Stock Input**: Enter ticker symbol for analysis
- **Real-time Progress**: See agents working in parallel
- **Agent Cards**: Individual agent status and signals
- **Results Panel**: Final recommendation with detailed rationale
- **Investor Advisor**: AI-generated plain-English advice

### Agent Deep Dive
Click "View Detailed Analysis" on any agent card to see:
- **Signal Visualization**: -1 (bearish) to +1 (bullish)
- **Confidence Gauge**: 0-100% reliability score
- **Sentiment Breakdown**: For sentiment agent (positive/neutral/negative)
- **News Articles**: Real articles with clickable links and images
- **Key Metrics**: All data points from the agent
- **Data Source Verification**: Confirms data is from real APIs

### Investor Advisor
- Synthesizes all agent insights
- Provides plain-English investment advice
- Identifies key opportunities and risks
- Suggests practical next steps
- Powered by Gemini AI

---

## 📁 Project Structure

```
Agent Capstone/
├── agents/                      # A2A Agent Servers
│   ├── fundamental_analyst_server.py
│   ├── technical_analyst_server.py
│   ├── news_sentiment_analyst_server.py
│   ├── macro_analyst_server.py
│   ├── regulatory_analyst_server.py
│   └── kaggle_orchestrator.py   # Main orchestrator
├── tools/                       # Data fetching tools
│   ├── polygon_fetcher.py       # Stock data from Polygon
│   ├── fred_fetcher.py          # Macro data from FRED
│   ├── news_fetcher.py          # News from multiple sources
│   └── sec_edgar_fetcher.py     # SEC filings
├── frontend/                    # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx            # Main dashboard
│   │   ├── components/         # React components
│   │   │   ├── AgentCard.tsx
│   │   │   ├── AgentDetailModal.tsx
│   │   │   ├── ResultsPanel.tsx
│   │   │   └── InvestorAdvisorCard.tsx
│   │   └── api/                # API routes
│   └── package.json
├── notebooks/                   # Jupyter notebooks
│   └── kaggle_submission_complete.ipynb  # Full demo
├── scripts/                     # Utility scripts
│   ├── start_all_agents.sh     # Start A2A servers
│   ├── stop_all_agents.sh      # Stop A2A servers
│   ├── start_full_system.sh    # Start backend + frontend
│   └── stop_full_system.sh     # Stop everything
├── main.py                      # CLI entry point
├── frontend_api.py              # Backend API wrapper
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🎓 Gen AI Capabilities Demonstrated

This project showcases **12+ advanced Gen AI capabilities** from the Kaggle 5-Day Agents course:

1. **Agent-to-Agent (A2A) Communication** - Full v0.3.0 protocol implementation
2. **Custom Tools** - Real API integrations (Polygon, FRED, NewsAPI, SEC)
3. **Structured Output** - Pydantic schemas for all responses
4. **Multi-Agent Orchestration** - Coordinator pattern with parallel execution
5. **Context Management** - Session handling across agents
6. **Streaming Responses** - Real-time progress updates
7. **Error Handling** - Graceful degradation and fallbacks
8. **Agent Cards** - JSONRPC metadata for discovery
9. **RAG (Retrieval-Augmented Generation)** - Knowledge bases in prompts
10. **Embeddings** - Semantic search for relevant data
11. **Document Understanding** - Parsing SEC filings
12. **Long Context Windows** - Leveraging Gemini's 2M token context
13. **Ensemble Learning** - Weighted signal synthesis
14. **Risk Assessment** - Confidence scoring and risk categorization

---

## 📈 Performance & Metrics

### Speed
- **Average analysis time**: 4-6 seconds
- **Agent startup**: < 2 seconds
- **Parallel execution**: All 5 specialist agents run simultaneously

### Accuracy
- **Confidence scores**: 60-75% (realistic, not overfit)
- **Signal differentiation**: Real variation per stock
- **Data freshness**: Real-time API calls

### Scalability
- **Microservices**: Each agent runs independently
- **Stateless design**: Easy horizontal scaling
- **API rate limits**: Respects provider quotas

---

## 🧪 Testing & Validation

### Verify Setup
```bash
python verify_setup.py
```

### Test Individual Agent
```bash
# Start agents
bash scripts/start_all_agents.sh

# Test fundamental agent
curl http://localhost:8001/agent-card

# Expected: JSON with agent metadata
```

### Run Full Analysis
```bash
./venv/bin/python main.py --ticker NVDA
```

### Frontend Testing
```bash
# Start full system
bash scripts/start_full_system.sh

# Open browser: http://localhost:3001
# Try: AAPL, NVDA, TSLA, etc.
```

---

## 🐛 Troubleshooting

### Python Version Error
```bash
# Error: A2A requires Python 3.10+
# Fix: Install Python 3.11
brew install python@3.11  # macOS
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Error: Address already in use
# Fix: Kill process on port
lsof -i :8000  # Find PID
kill -9 <PID>  # Kill process
```

### API Key Errors
```bash
# Check if keys are set
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Google:', bool(os.getenv('GOOGLE_API_KEY'))); print('Polygon:', bool(os.getenv('POLYGON_API_KEY')))"
```

### Frontend Build Errors
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### Agent Connection Errors
```bash
# Restart all agents
bash scripts/stop_all_agents.sh
sleep 2
bash scripts/start_all_agents.sh
```

---

## 📝 Kaggle Submission

### Jupyter Notebook
The complete project demonstration is in:
```
notebooks/kaggle_submission_complete.ipynb
```

This notebook includes:
- ✅ Executive summary and architecture
- ✅ 12+ Gen AI capabilities explained
- ✅ Live ticker analysis with transparent outputs
- ✅ All 7 agent responses displayed
- ✅ Investor advisor AI explanation
- ✅ Performance metrics and evaluation

### Running the Notebook
```bash
# Start Jupyter
jupyter notebook

# Open: notebooks/kaggle_submission_complete.ipynb
# Run all cells to see complete demo
```

---

## 🎨 UI Design

The frontend features a professional dark theme with:
- **Glassmorphism effects** for modern appearance
- **Gradient borders** inspired by shadcn/ui
- **Real-time animations** for agent status
- **Responsive design** for all screen sizes
- **Accessible colors** with high contrast
- **Professional typography** using Inter font

---

## 🔐 Security Best Practices

1. ✅ **Never commit `.env`** (already in `.gitignore`)
2. ✅ **Use environment variables** in production
3. ✅ **Rotate API keys** periodically
4. ✅ **Set usage limits** in API dashboards
5. ✅ **Monitor API costs** regularly
6. ✅ **Input validation** on all user inputs
7. ✅ **Rate limiting** on API endpoints

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Authors

**Nishant Pithia & Vagge Sneha**

Kaggle 5-Day Agents Intensive - Capstone Project

---

## 🙏 Acknowledgments

- Google ADK and Gemini team
- Kaggle for the 5-Day Agents course
- Polygon.io for comprehensive market data
- FRED API for economic indicators
- NewsAPI for sentiment analysis data

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review Jupyter notebook for examples
3. Check agent logs in the terminal
4. Verify API keys are set correctly

---

**Built with ❤️ using Google ADK, Gemini, and the A2A Protocol**
