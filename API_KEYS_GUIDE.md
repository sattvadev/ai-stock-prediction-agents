# 🔑 API Keys Setup Guide

## Required API Keys

### 1. **GOOGLE_API_KEY** ✅ **REQUIRED**
- **What:** Google Gemini API access
- **Used for:** All 7 AI agents (Gemini-2.0-flash-exp model)
- **Get it:** https://aistudio.google.com/apikey
- **Cost:** Free tier available, then pay-as-you-go

```bash
GOOGLE_API_KEY=AIza...your_key_here
```

---

### 2. **POLYGON_API_KEY** ✅ **REQUIRED**
- **What:** Polygon.io market data API
- **Used for:**
  - Stock prices & historical data
  - Fundamental metrics (P/E, EPS, revenue, etc.)
  - Technical indicators (RSI, MACD, Bollinger Bands)
  - **News articles** (built-in news endpoint)
- **Get it:** https://polygon.io/dashboard/api-keys
- **Cost:** You already have paid account

```bash
POLYGON_API_KEY=your_polygon_key_here
```

**✨ Polygon provides news, so you DON'T need a separate news API!**

---

## Optional API Keys

### 3. **FRED_API_KEY** ⚠️ **RECOMMENDED** (Free)
- **What:** Federal Reserve Economic Data API
- **Used for:**
  - GDP growth rates
  - Inflation (CPI)
  - Federal Funds Rate
  - Treasury yields
- **Get it:** https://fred.stlouisfed.org/docs/api/api_key.html
- **Cost:** **Completely FREE**
- **Why separate from Polygon:** Polygon doesn't have macro-economic indicators

```bash
FRED_API_KEY=your_fred_key_here
```

---

### 4. **NEWS_API_KEY** ⚠️ **OPTIONAL**
- **What:** NewsAPI.org access
- **Used for:** Alternative news source (primary source if provided)
- **Get it:** https://newsapi.org/register
- **Cost:** Free tier = 100 requests/day
- **Status:** **NOT NEEDED** - Polygon already provides news
- **Fallback chain:** NewsAPI → Polygon News → Google News RSS

```bash
NEWS_API_KEY=your_newsapi_key_here  # Optional - leave blank to use Polygon
```

---

## Summary: What You Actually Need

### Minimum Setup (2 keys):
```bash
GOOGLE_API_KEY=...   # For Gemini AI
POLYGON_API_KEY=...  # For all market data + news
```

### Recommended Setup (3 keys):
```bash
GOOGLE_API_KEY=...   # For Gemini AI
POLYGON_API_KEY=...  # For market data + news
FRED_API_KEY=...     # For macro data (FREE!)
```

### Full Setup (4 keys):
```bash
GOOGLE_API_KEY=...   # For Gemini AI
POLYGON_API_KEY=...  # For market data + news
FRED_API_KEY=...     # For macro data (FREE!)
NEWS_API_KEY=...     # Optional alternative news source
```

---

## How the System Uses These Keys

### Data Flow by Agent:

| Agent | Primary Data Source | API Key Used |
|-------|-------------------|--------------|
| **Fundamental Analyst** | Polygon fundamentals + SEC filings | POLYGON_API_KEY |
| **Technical Analyst** | Polygon price data + TA-Lib | POLYGON_API_KEY |
| **Sentiment Analyst** | Polygon News API | POLYGON_API_KEY (or NEWS_API_KEY) |
| **Macro Analyst** | FRED API | FRED_API_KEY |
| **Regulatory Analyst** | SEC EDGAR (free) + News | POLYGON_API_KEY |
| **Predictor Agent** | ML Model synthesis | N/A |
| **Strategist** | Orchestration | N/A |

**All agents use:** GOOGLE_API_KEY for Gemini LLM reasoning

---

## Configuration Steps

1. **Copy the example:**
```bash
cp .env.example .env
```

2. **Edit .env and add your keys:**
```bash
nano .env  # or use any text editor
```

3. **Verify setup:**
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Google API:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'MISSING'); print('Polygon API:', 'SET' if os.getenv('POLYGON_API_KEY') else 'MISSING')"
```

---

## Cost Estimates (Typical Usage)

### Per Stock Analysis:
- **Google Gemini:** ~$0.02 - $0.05 per analysis
- **Polygon API:** ~5-10 API calls (covered by subscription)
- **FRED API:** FREE (no limits for non-commercial use)
- **Total per analysis:** ~$0.02 - $0.05

### 100 Analyses:
- **Cost:** ~$2 - $5 (mostly Gemini)

---

## Troubleshooting

### Error: "GOOGLE_API_KEY not found"
```bash
# Check if .env exists
ls -la .env

# Verify key is set
grep GOOGLE_API_KEY .env
```

### Error: "POLYGON_API_KEY not set"
- Make sure you copied `.env.example` to `.env`
- Ensure no spaces around the `=` sign
- Verify key from Polygon dashboard

### News fetching fails
- System automatically falls back to Polygon news
- Then to Google News RSS (no key needed)
- Check logs for specific error messages

---

## Security Best Practices

1. ✅ **Never commit `.env` to git** (already in `.gitignore`)
2. ✅ **Use environment variables in production**
3. ✅ **Rotate API keys periodically**
4. ✅ **Set usage limits in API dashboards**
5. ✅ **Monitor API costs regularly**

---

**Questions? Check `README.md` or `SETUP_INSTRUCTIONS.md`**

