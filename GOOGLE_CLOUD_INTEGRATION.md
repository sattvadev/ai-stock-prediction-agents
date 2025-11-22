# 🌐 Google Cloud Platform Integration Guide

Complete guide to deploying your chatbot and exposing agents to Google's ecosystem, plus subscribing to external agents.

## 🎯 Overview

This guide covers:
1. **Deploying chatbot to Google Cloud Run**
2. **Exposing agents to Google ecosystem** (Vertex AI, Marketplace)
3. **Subscribing to external A2A agents** via agent registry
4. **Integration with Vertex AI Agent Builder**

## 🚀 Part 1: Deploy Chatbot to Cloud Run

### Prerequisites

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 1: Store Secrets

```bash
# Store API keys in Secret Manager
echo -n "your-google-api-key" | gcloud secrets create GOOGLE_API_KEY --data-file=-
echo -n "your-polygon-key" | gcloud secrets create POLYGON_API_KEY --data-file=-
```

### Step 2: Deploy Agents First

Your agents must be deployed before the chatbot:

```bash
# Deploy all agents (from your existing cloudbuild.yaml)
gcloud builds submit --config=deploy/cloudbuild.yaml

# Get agent URLs
FUNDAMENTAL_URL=$(gcloud run services describe fundamental-agent --region=us-central1 --format='value(status.url)')
TECHNICAL_URL=$(gcloud run services describe technical-agent --region=us-central1 --format='value(status.url)')
# ... etc
```

### Step 3: Deploy Agent Registry

```bash
# Build and deploy registry
gcloud builds submit --config=deploy/cloudbuild-chatbot.yaml --substitutions=_REGION=us-central1

# Get registry URL
REGISTRY_URL=$(gcloud run services describe agent-registry --region=us-central1 --format='value(status.url)')
```

### Step 4: Deploy Chatbot

```bash
# Set environment variables with agent URLs
gcloud run deploy stock-chatbot \
  --image=gcr.io/YOUR_PROJECT_ID/stock-chatbot:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FUNDAMENTAL_AGENT_URL=$FUNDAMENTAL_URL,TECHNICAL_AGENT_URL=$TECHNICAL_URL,SENTIMENT_AGENT_URL=$SENTIMENT_URL,MACRO_AGENT_URL=$MACRO_URL,REGULATORY_AGENT_URL=$REGULATORY_URL,PREDICTOR_AGENT_URL=$PREDICTOR_URL,AGENT_REGISTRY_URL=$REGISTRY_URL" \
  --set-secrets="GOOGLE_API_KEY=GOOGLE_API_KEY:latest" \
  --memory=2Gi \
  --cpu=2 \
  --timeout=600 \
  --max-instances=20 \
  --min-instances=1

# Get chatbot URL
CHATBOT_URL=$(gcloud run services describe stock-chatbot --region=us-central1 --format='value(status.url)')
echo "Chatbot available at: $CHATBOT_URL"
```

### Step 5: Test Deployment

```bash
# Test chatbot
curl -X POST "$CHATBOT_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze AAPL fundamentals"}'

# Check health
curl "$CHATBOT_URL/health"

# List external agents
curl "$CHATBOT_URL/agents/external"
```

## 🔍 Part 2: Expose Agents to Google Ecosystem

### Option A: Vertex AI Agent Builder Integration

Your agents are already A2A-compatible. Integrate with Vertex AI:

```bash
# Enable Vertex AI
gcloud services enable aiplatform.googleapis.com

# Create Vertex AI agent that uses your A2A agents
gcloud ai agents create \
  --display-name="Stock Prediction System" \
  --config=deploy/vertex-agent-config.yaml \
  --region=us-central1
```

**Vertex AI Agent Builder Benefits:**
- Visual agent designer
- Native Google integration
- Automatic scaling
- Advanced monitoring
- Integration with Google services (Search, Workspace, etc.)

### Option B: Google Cloud Marketplace

Publish your agents to Google Cloud Marketplace:

1. **Prepare Agent Package:**
```yaml
# marketplace/agent-package.yaml
apiVersion: v1
kind: AgentPackage
metadata:
  name: stock-prediction-agents
  displayName: Stock Prediction Multi-Agent System
spec:
  agents:
    - name: fundamental-analyst
      description: Financial metrics and valuation analysis
      agentCardUrl: https://fundamental-agent-xxx.run.app/.well-known/agent-card.json
    - name: technical-analyst
      description: Technical indicators and price analysis
      agentCardUrl: https://technical-agent-xxx.run.app/.well-known/agent-card.json
  # ... more agents
```

2. **Submit to Marketplace:**
```bash
# Follow Google Cloud Marketplace partner process
# https://cloud.google.com/marketplace/docs/partners/ai-agents
```

### Option C: A2A Agent Registry (Your Own)

Your `agent_registry.py` service acts as a discovery mechanism:

```bash
# Register your agents
curl -X POST "$REGISTRY_URL/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "fundamental-analyst",
    "name": "Fundamental Analyst",
    "description": "Financial metrics and valuation analysis",
    "agent_card_url": "https://fundamental-agent-xxx.run.app/.well-known/agent-card.json",
    "category": "financial",
    "provider": "your-org"
  }'
```

## 🔗 Part 3: Subscribe to External Agents

### Step 1: Discover External Agents

```bash
# Discover agent by URL
curl -X POST "$REGISTRY_URL/agents/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_card_url": "https://external-agent.example.com/.well-known/agent-card.json",
    "category": "intelligence"
  }'

# Search for agents
curl "$REGISTRY_URL/agents/search?query=market+intelligence&category=intelligence"
```

### Step 2: Register External Agent

```bash
# Register external agent
curl -X POST "$REGISTRY_URL/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "market-intelligence-agent",
    "name": "Market Intelligence Agent",
    "description": "Advanced market insights and trend analysis",
    "agent_card_url": "https://external-provider.com/agents/intelligence/.well-known/agent-card.json",
    "category": "intelligence",
    "provider": "external-partner",
    "tags": ["market", "intelligence", "trends"]
  }'
```

### Step 3: Chatbot Auto-Discovers

The chatbot automatically discovers external agents on startup:

```python
# chatbot_cloud.py calls discover_external_agents() on startup
# External agents become available as functions to Gemini
```

### Step 4: Use External Agent in Chat

```bash
# Chatbot will automatically use external agents when appropriate
curl -X POST "$CHATBOT_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get market intelligence insights for tech stocks"
  }'

# Gemini will call call_external_market-intelligence-agent() function
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Google Cloud Platform                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │   Chatbot    │───▶│   Registry   │                 │
│  │ (Cloud Run)  │    │ (Cloud Run)  │                 │
│  └──────┬───────┘    └──────┬───────┘                 │
│         │                    │                          │
│         │                    │                          │
│    ┌────▼────────────────────▼────┐                    │
│    │   Internal A2A Agents        │                    │
│    │  (Fundamental, Technical...)  │                    │
│    └──────────────────────────────┘                    │
│         │                                               │
│         │                                               │
│    ┌────▼──────────────────────────┐                    │
│    │   External A2A Agents        │                    │
│    │  (Discovered via Registry)   │                    │
│    └──────────────────────────────┘                    │
│                                                         │
│  ┌──────────────────────────────────┐                   │
│  │   Vertex AI Agent Builder       │                   │
│  │   (Optional Integration)        │                   │
│  └──────────────────────────────────┘                   │
│                                                         │
│  ┌──────────────────────────────────┐                   │
│  │   Google Cloud Marketplace       │                   │
│  │   (Agent Publishing)              │                   │
│  └──────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

## 🔐 Security & Authentication

### For Production:

```bash
# Require authentication
gcloud run services update stock-chatbot \
  --region=us-central1 \
  --no-allow-unauthenticated

# Use IAM
gcloud run services add-iam-policy-binding stock-chatbot \
  --region=us-central1 \
  --member="user:your-email@example.com" \
  --role="roles/run.invoker"
```

### Agent-to-Agent Security:

```python
# Add authentication headers when calling external agents
headers = {
    "Authorization": f"Bearer {agent_api_key}",
    "X-Agent-ID": "your-agent-id"
}
```

## 📊 Monitoring

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=stock-chatbot" --limit=50

# View metrics
gcloud monitoring dashboards create --config-from-file=dashboard.json
```

## 🎯 Example: Complete Workflow

```bash
# 1. Deploy everything
gcloud builds submit --config=deploy/cloudbuild-chatbot.yaml

# 2. Register external agent
curl -X POST "$REGISTRY_URL/agents/register" \
  -d @external-agent-registration.json

# 3. Chatbot discovers it automatically
curl "$CHATBOT_URL/agents/external"

# 4. Use in chat
curl -X POST "$CHATBOT_URL/chat" \
  -d '{"message": "Analyze AAPL with market intelligence"}'

# 5. Monitor
gcloud logging read "resource.type=cloud_run_revision" --limit=10
```

## 🌍 Multi-Region Deployment

```bash
# Deploy to multiple regions
for region in us-central1 europe-west1 asia-northeast1; do
  gcloud builds submit \
    --config=deploy/cloudbuild-chatbot.yaml \
    --substitutions=_REGION=$region
done

# Set up Cloud Load Balancer
gcloud compute backend-services create chatbot-backend \
  --global

# Add regions to backend
for region in us-central1 europe-west1 asia-northeast1; do
  gcloud compute backend-services add-backend chatbot-backend \
    --global \
    --network-endpoint-group=chatbot-neg-$region \
    --network-endpoint-group-region=$region
done
```

## 📝 Next Steps

1. **Publish to Marketplace**: Follow Google Cloud Marketplace partner process
2. **Integrate Vertex AI**: Use Vertex AI Agent Builder for visual design
3. **Add More External Agents**: Discover and subscribe to more agents
4. **Implement Caching**: Add Redis for agent response caching
5. **Add Analytics**: Track agent usage and performance

---

**Built for Google Cloud Platform** • **A2A Protocol** • **Vertex AI** • **Cloud Run**

