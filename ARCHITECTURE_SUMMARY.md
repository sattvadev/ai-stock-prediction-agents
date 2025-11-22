# 🏗️ System Architecture Summary

## LLM: Google Gemini

**All 7 agents powered by:**
```python
model=Gemini(model="gemini-2.0-flash-exp")
```

**Why Gemini?**
- ✅ 1M+ token context window (handle long SEC filings)
- ✅ Native function calling support
- ✅ JSON mode for structured outputs
- ✅ Fast inference (flash models)
- ✅ Built for Google ADK framework

---

## Data Sources Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                           │
└─────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Polygon.io  │  │   FRED API   │  │  SEC EDGAR   │  │  News APIs   │
│  (Primary)   │  │   (Macro)    │  │   (Free)     │  │ (Fallback)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │                 │
       ├─ Price Data    ├─ GDP            ├─ 10-K          ├─ Polygon News
       ├─ Fundamentals  ├─ Inflation      ├─ 10-Q          ├─ NewsAPI
       ├─ News          ├─ Fed Rates      ├─ 8-K           └─ Google News RSS
       └─ Indicators    └─ Treasury       └─ Risk Factors

                              ▼

┌─────────────────────────────────────────────────────────┐
│              Custom Tool Layer (Python)                 │
│                                                         │
│  • polygon_fetcher.py    → Polygon API wrapper         │
│  • fred_fetcher.py       → FRED API wrapper            │
│  • sec_edgar_fetcher.py  → SEC filing parser           │
│  • news_fetcher.py       → Multi-source news           │
│  • technical_indicators  → TA-Lib calculations         │
└─────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────┐
│             Agent Layer (Google ADK + A2A)              │
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │  The Strategist (Orchestrator)               │      │
│  │  • Uses: RemoteA2aAgent for coordination    │      │
│  │  • Model: Gemini-2.0-flash-exp              │      │
│  └──────────────────┬───────────────────────────┘      │
│                     │                                   │
│        ┌────────────┴─────────────────┐                │
│        ▼                               ▼                │
│  ┌─────────────┐              ┌──────────────┐         │
│  │ Fundamental │              │  Technical   │         │
│  │  Analyst    │              │   Analyst    │         │
│  │ Port: 8001  │              │  Port: 8002  │         │
│  │ Tools:      │              │  Tools:      │         │
│  │ • Polygon   │              │ • Polygon    │         │
│  │ • SEC       │              │ • TA-Lib     │         │
│  └─────────────┘              └──────────────┘         │
│        ▼                               ▼                │
│  ┌─────────────┐              ┌──────────────┐         │
│  │ Sentiment   │              │    Macro     │         │
│  │  Analyst    │              │   Analyst    │         │
│  │ Port: 8003  │              │  Port: 8004  │         │
│  │ Tools:      │              │  Tools:      │         │
│  │ • News API  │              │ • FRED       │         │
│  └─────────────┘              └──────────────┘         │
│        ▼                               ▼                │
│  ┌─────────────┐              ┌──────────────┐         │
│  │ Regulatory  │              │  Predictor   │         │
│  │  Analyst    │              │    Agent     │         │
│  │ Port: 8005  │              │  Port: 8006  │         │
│  │ Tools:      │              │  Tools:      │         │
│  │ • SEC       │              │ • XGBoost ML │         │
│  │ • News      │              │ • Risk Calc  │         │
│  └─────────────┘              └──────────────┘         │
└─────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────┐
│               Output Layer                              │
│                                                         │
│  • CLI (main.py)                                       │
│  • Jupyter Notebook (stock_prediction_capstone.ipynb)  │
│  • JSON/Pydantic structured reports                    │
└─────────────────────────────────────────────────────────┘
```

---

## Detailed Data Source Mapping

### 1. Polygon.io API (Primary) - YOU HAVE PAID ACCOUNT ✅
**Endpoints Used:**
- `/v2/aggs/ticker/{ticker}/range` → Historical OHLCV data
- `/v3/reference/financials` → Balance sheet, income statement, cash flow
- `/v2/reference/news` → **News articles with sentiment**
- Custom calculations → RSI, MACD, Bollinger Bands (via TA-Lib)

**Agents Using Polygon:**
- Fundamental Analyst (financials)
- Technical Analyst (price data)
- Sentiment Analyst (news)
- Regulatory Analyst (news)

---

### 2. FRED API (Federal Reserve) - FREE ✅
**Series IDs Used:**
- `A191RL1Q225SBEA` → GDP Growth Rate
- `CPIAUCSL` → Consumer Price Index (Inflation)
- `FEDFUNDS` → Federal Funds Rate
- `DGS10` → 10-Year Treasury Yield

**Agents Using FRED:**
- Macro-Economic Analyst

**Why not from Polygon?**
- Polygon doesn't provide macroeconomic indicators
- FRED is the authoritative government source
- Completely free with generous rate limits

---

### 3. SEC EDGAR (Free, No Key) ✅
**Filings Parsed:**
- 10-K (Annual Reports)
- 10-Q (Quarterly Reports)
- 8-K (Current Events)

**Sections Extracted:**
- Risk Factors (Item 1A)
- Management Discussion & Analysis (MD&A)
- Financial Statements

**Agents Using SEC:**
- Fundamental Analyst (financial statements)
- Regulatory Analyst (risk factors, legal issues)

---

### 4. News Sources (Fallback Chain) ⚠️
**Priority Order:**

1. **NewsAPI.org** (if `NEWS_API_KEY` is set)
   - Used by: Sentiment Analyst
   - Rate limit: 100 requests/day (free), 1000/day (paid)

2. **Polygon News** ✅ **YOUR PRIMARY NEWS SOURCE**
   - Used by: Sentiment Analyst, Regulatory Analyst
   - Included in your Polygon subscription
   - Better for financial news (already filtered by ticker)

3. **Google News RSS** (last resort, no key needed)
   - Used by: All news-dependent agents
   - Scraping-based fallback
   - Free, unlimited

**Current Implementation:**
```python
# news_fetcher.py tries in order:
1. NewsAPI (if key exists) → NewsAPI.org
2. Polygon News → Your paid API
3. Google News RSS → Free scraping
```

**Recommendation:** Leave `NEWS_API_KEY` blank and rely on Polygon News

---

## API Cost Breakdown

### Per Stock Analysis:

| Service | Calls per Analysis | Cost per Call | Total Cost |
|---------|-------------------|---------------|------------|
| **Google Gemini** | ~7-10 LLM calls | ~$0.002-$0.005 | ~$0.02-$0.05 |
| **Polygon API** | ~5-10 endpoints | Subscription | $0 (covered) |
| **FRED API** | ~4 series | FREE | $0 |
| **SEC EDGAR** | ~1-2 filings | FREE | $0 |
| **Total** | | | **~$0.02-$0.05** |

### 100 Stock Analyses:
- **Cost:** ~$2-$5 (almost entirely Gemini)
- **Polygon:** Covered by your subscription
- **FRED + SEC:** FREE

---

## Why This Architecture?

### ✅ Advantages:

1. **Cost Efficiency**
   - Most data sources are free (FRED, SEC)
   - Polygon covers multiple needs in one subscription
   - Only pay for Gemini inference

2. **Data Quality**
   - Polygon: Professional-grade financial data
   - FRED: Official government economic data
   - SEC: Primary source for corporate disclosures

3. **Redundancy**
   - News has 3 fallback sources
   - Polygon provides both price + fundamentals + news
   - No single point of failure

4. **Scalability**
   - A2A protocol allows agents to scale independently
   - Can run agents on different machines/containers
   - Easy to add new data sources or agents

5. **Compliance**
   - Using official, legal data sources
   - SEC EDGAR is the authoritative source for filings
   - No unauthorized scraping of proprietary data

---

## What You Need to Start

### Minimum (2 API keys):
```bash
GOOGLE_API_KEY=...    # Get from ai.google.dev
POLYGON_API_KEY=...   # You already have this!
```

### Recommended (3 API keys):
```bash
GOOGLE_API_KEY=...    # Get from ai.google.dev
POLYGON_API_KEY=...   # You already have this!
FRED_API_KEY=...      # Get FREE from fred.stlouisfed.org
```

### Optional (4 API keys):
```bash
NEWS_API_KEY=...      # Only if you want NewsAPI instead of Polygon news
```

---

## Quick Start

1. **Configure API keys:**
```bash
cd "/Users/pithia/Documents/Dev/Agent Capstone"
cp .env.example .env
nano .env  # Add your GOOGLE_API_KEY and POLYGON_API_KEY
```

2. **Start all agents:**
```bash
bash scripts/start_all_agents.sh
```

3. **Run analysis:**
```bash
python main.py --ticker GOOGL --verbose
```

---

**See also:**
- `API_KEYS_GUIDE.md` - Detailed API key setup
- `README.md` - Full project documentation
- `SETUP_INSTRUCTIONS.md` - Step-by-step setup guide

