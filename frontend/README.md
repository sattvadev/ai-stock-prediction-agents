# 🎨 Stock Prediction System - Frontend

Beautiful, modern Next.js frontend with glassmorphic design for the multi-agent stock prediction system.

## ✨ Features

- **Glassmorphic UI**: Apple-inspired design with backdrop blur effects
- **Real-time Agent Status**: Watch agents work with animated progress indicators
- **Smooth Animations**: Framer Motion for fluid transitions
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Live API Integration**: Connects to Python backend via REST API
- **TypeScript**: Full type safety throughout

## 🏗️ Tech Stack

- **Next.js 14** with App Router
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Lucide React** for icons
- **Axios** for API calls

## 📁 Project Structure

```
frontend/
├── app/
│   ├── components/
│   │   ├── StockInput.tsx       # Stock ticker input form
│   │   ├── OrchestratorCard.tsx # Orchestrator status display
│   │   ├── AgentCard.tsx        # Individual agent cards
│   │   └── ResultsPanel.tsx     # Final results display
│   ├── api/
│   │   └── analyze/
│   │       └── route.ts         # API endpoint for analysis
│   ├── types/
│   │   └── index.ts             # TypeScript interfaces
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Main page
│   └── globals.css              # Global styles
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── next.config.js
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- Python backend running (see main README)
- All A2A agents running on ports 8001-8006

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at **http://localhost:3000**

## 🔧 Configuration

### Environment Variables

Create `.env.local` in the frontend directory (optional):

```env
PYTHON_BACKEND_URL=http://localhost:8000
```

### Backend Connection

The frontend expects the Python FastAPI backend to be running on **http://localhost:8000**.

To start the backend:

```bash
# From project root
./venv/bin/python frontend_api.py
```

## 🎯 Usage Flow

1. **Enter Stock Ticker**: Type a stock symbol (e.g., GOOGL, AAPL, NVDA)
2. **Watch Agents Work**: See the orchestrator coordinate 6 specialist agents
3. **View Results**: Get AI-powered recommendation with confidence score
4. **Explore Details**: Expand to see individual agent responses

## 🎨 Design System

### Colors

- **Primary**: Purple/Blue gradients
- **Success**: Green (BUY signals)
- **Warning**: Yellow/Orange (HOLD signals)
- **Danger**: Red (SELL signals)

### Glass Effects

```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Animations

- **Pulse**: For loading indicators
- **Shimmer**: For progress bars
- **Fade/Slide**: For page transitions
- **Scale**: For hover effects

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (single column)
- **Tablet**: 768px - 1024px (2 columns)
- **Desktop**: > 1024px (3 columns)

## 🔌 API Integration

### POST /api/analyze

Request:
```json
{
  "ticker": "GOOGL",
  "horizon": "next_quarter"
}
```

Response:
```json
{
  "ticker": "GOOGL",
  "recommendation": "BUY",
  "confidence": 67.4,
  "weighted_signal": 0.273,
  "risk_level": "MEDIUM",
  "rationale": "...",
  "analysis_reports": {
    "fundamental": {...},
    "technical": {...},
    ...
  },
  "elapsed_seconds": 4.5
}
```

## 🧩 Components

### StockInput

Stock ticker input form with popular stock suggestions.

```tsx
<StockInput
  onAnalyze={(ticker) => handleAnalyze(ticker)}
  isLoading={false}
/>
```

### OrchestratorCard

Displays orchestrator status with progress bar.

```tsx
<OrchestratorCard
  ticker="GOOGL"
  status={{
    status: 'analyzing',
    message: 'Coordinating agents...',
    progress: 50
  }}
/>
```

### AgentCard

Individual agent status with results.

```tsx
<AgentCard
  agent={{
    id: 'fundamental',
    name: 'Fundamental Analyst',
    status: 'completed',
    progress: 100,
    signal: 0.40,
    confidence: 78
  }}
  icon="📊"
  color="from-blue-500 to-cyan-500"
  delay={0.1}
/>
```

### ResultsPanel

Final prediction results with Gemini synthesis.

```tsx
<ResultsPanel
  result={analysisResult}
  onReset={() => handleReset()}
/>
```

## 🎭 States

### Agent States

- **idle**: Not started
- **working**: Currently analyzing
- **completed**: Analysis finished
- **error**: Failed

### Orchestrator States

- **idle**: Waiting
- **initializing**: Starting up
- **analyzing**: Coordinating agents
- **synthesizing**: Final prediction
- **completed**: Done
- **error**: Failed

## 🚀 Deployment

### Build for Production

```bash
npm run build
npm start
```

### Deploy to Vercel

```bash
vercel
```

Make sure to set `PYTHON_BACKEND_URL` environment variable to your deployed backend.

## 🐛 Troubleshooting

### "Failed to analyze stock"

- Ensure Python backend is running on port 8000
- Check all A2A agents are online: `./scripts/start_all_agents.sh`
- Verify API keys in `.env`

### Styling Issues

```bash
# Rebuild Tailwind
npm run dev
```

### TypeScript Errors

```bash
# Check types
npm run build
```

## 📄 License

Part of the Stock Prediction System capstone project.

## 👥 Authors

**Nishant Pithia & Vagge Sneha**

---

Built with ❤️ using Next.js, Tailwind CSS, and Framer Motion

