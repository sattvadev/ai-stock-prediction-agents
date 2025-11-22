# 🚀 Vertex AI & Google Cloud Deployment

**Deploy your multi-agent stock prediction system to production in 15 minutes!**

## 🎯 What You'll Deploy

A fully-managed, auto-scaling multi-agent AI system with:

- ✅ **6 Specialist Agents** running on Cloud Run
- ✅ **Beautiful Agentic UI** showing real-time workflow
- ✅ **Vertex AI Integration** with A2A protocol
- ✅ **Production-Ready Infrastructure** with monitoring
- ✅ **Cost-Optimized** with auto-scaling to zero

## ⚡ Quick Start (15 minutes)

### 1. Prerequisites (2 min)

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**Required API Keys:**
- Google AI (Gemini): https://aistudio.google.com/apikey (FREE)
- Polygon.io: https://polygon.io (you already have this)

**Optional but recommended:**
- FRED API: https://fred.stlouisfed.org/docs/api/api_key.html (FREE)
- NewsAPI: https://newsapi.org/register (FREE)

### 2. Deploy Backend (10 min)

```bash
cd "Agent Capstone"
./deploy/deploy.sh
```

This will:
1. Enable required GCP APIs
2. Create secrets for API keys
3. Build Docker containers
4. Deploy 6 agent services
5. Deploy orchestrator
6. Configure auto-scaling

### 3. Deploy UI (3 min)

```bash
./deploy/deploy-vertex-ui.sh
```

This deploys:
- Beautiful dark-theme UI
- Real-time agent workflow visualization
- Execution timeline
- Results dashboard

### 4. Test It!

```bash
# Open your deployed UI
gcloud app browse

# Or test the API directly
export ORCHESTRATOR_URL=$(gcloud run services describe orchestrator --region=us-central1 --format='value(status.url)')
curl "$ORCHESTRATOR_URL/api/analyze?ticker=AAPL"
```

## 🎨 Agentic UI Features

Your deployed UI includes stunning visualizations:

### 1. **Agent Workflow Cards**
Each agent displays:
- Real-time status (waiting → working → complete)
- Signal strength with color-coded bars
- Confidence percentage
- Visual pulse animation while working

### 2. **Execution Timeline**
- Timestamped events
- Agent start/completion tracking
- Phase transitions
- Final synthesis steps

### 3. **Results Dashboard**
- Large recommendation badge (BUY/HOLD/SELL)
- Animated confidence meter
- Detailed rationale
- Risk assessment

### 4. **Beautiful Design**
- Glassmorphism effects
- Gradient borders
- Dark theme optimized
- Smooth animations
- Mobile responsive

## 🏗️ Architecture

```
User Browser
    ↓
App Engine (UI) - https://YOUR-PROJECT.uc.r.appspot.com
    ↓
Cloud Run (Orchestrator) - Coordinates everything
    ↓
┌──────┬──────┬──────┬──────┬──────┬──────┐
│Fund  │Tech  │Sent  │Macro │Reg   │Pred  │
│Agent │Agent │Agent │Agent │Agent │Agent │
└──────┴──────┴──────┴──────┴──────┴──────┘
    ↓
External APIs: Polygon, FRED, NewsAPI, SEC, Gemini
```

### Service Details

| Service | Purpose | Scaling | Memory | Timeout |
|---------|---------|---------|--------|---------|
| **fundamental-agent** | Financial analysis | 0-10 | 1GB | 300s |
| **technical-agent** | Price trends | 0-10 | 1GB | 300s |
| **sentiment-agent** | News analysis | 0-10 | 1GB | 300s |
| **macro-agent** | Economic factors | 0-10 | 1GB | 300s |
| **regulatory-agent** | Compliance | 0-10 | 1GB | 300s |
| **predictor-agent** | Synthesis | 0-10 | 1GB | 300s |
| **orchestrator** | Coordination | 1-20 | 2GB | 600s |
| **ui** | Frontend | 0-5 | 256MB | N/A |

## 💰 Cost Estimates

### Free Tier (Typical for personal use)
- First 2M requests: **FREE**
- 360K GB-seconds: **FREE**
- Expected cost: **$0-5/month**

### Light Production (< 100 analyses/day)
- Cloud Run: $3-5
- App Engine: $5-8
- Storage: $1
- **Total: $9-14/month**

### Medium Production (< 1000 analyses/day)
- Cloud Run: $10-15
- App Engine: $8-12
- Storage: $2
- **Total: $20-29/month**

### Heavy Production (> 1000 analyses/day)
- Cloud Run: $20-40
- App Engine: $12-20
- Storage: $3
- **Total: $35-63/month**

**Cost optimization tips:**
- Services scale to zero when idle
- Use Cloud Scheduler to keep warm if needed
- Enable caching for repeated queries
- Set up budget alerts

## 🔧 Configuration

### Update Agent URLs

After deployment, agent URLs are automatically configured. To manually update:

```bash
gcloud run services update orchestrator \
  --set-env-vars="FUNDAMENTAL_AGENT_URL=https://fundamental-agent-xxx.run.app" \
  --region=us-central1
```

### Adjust Scaling

```bash
# More aggressive scaling
gcloud run services update orchestrator \
  --max-instances=50 \
  --min-instances=2 \
  --region=us-central1

# Scale to zero (cost savings)
gcloud run services update fundamental-agent \
  --min-instances=0 \
  --region=us-central1
```

### Update Resources

```bash
# More memory for heavy loads
gcloud run services update orchestrator \
  --memory=4Gi \
  --cpu=4 \
  --region=us-central1
```

## 📊 Monitoring

### View Real-Time Logs

```bash
# Orchestrator logs
gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=orchestrator'

# All services
gcloud logging tail 'resource.type=cloud_run_revision'

# Errors only
gcloud logging tail 'resource.type=cloud_run_revision AND severity>=ERROR'
```

### Metrics Dashboard

```bash
# Open Cloud Console
gcloud console cloud-monitoring
```

Key metrics to monitor:
- **Request count**: Total analyses
- **Latency**: p50, p95, p99
- **Error rate**: < 1% is good
- **Instance count**: Auto-scaling activity
- **Memory usage**: Detect leaks
- **CPU usage**: Performance issues

### Set Up Alerts

```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
  --display-name="High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --notification-channels=CHANNEL_ID
```

## 🔐 Security

### API Key Management

API keys are stored in Secret Manager:

```bash
# View secrets
gcloud secrets list

# Update a secret
echo -n "new_api_key" | gcloud secrets versions add GOOGLE_API_KEY --data-file=-

# Access requires IAM permissions
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Enable Authentication

By default, services are public. To restrict access:

```bash
# Remove public access
gcloud run services remove-iam-policy-binding orchestrator \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1

# Add specific users
gcloud run services add-iam-policy-binding orchestrator \
  --member="user:your-email@gmail.com" \
  --role="roles/run.invoker" \
  --region=us-central1
```

### Add Rate Limiting

```bash
# Create Cloud Armor policy
gcloud compute security-policies create rate-limit \
  --description="Rate limit for stock analysis"

# Add rate limit rule
gcloud compute security-policies rules create 1000 \
  --security-policy=rate-limit \
  --action="rate-based-ban" \
  --rate-limit-threshold-count=100 \
  --rate-limit-threshold-interval-sec=60
```

## 🧪 Testing

### Automated Testing

```bash
./deploy/test-deployment.sh
```

Runs:
- Health checks for all services
- Sample analysis (AAPL)
- Performance test (GOOGL)
- UI accessibility test

### Manual Testing

```bash
# Health check
curl https://orchestrator-xxx.run.app/health

# Single analysis
curl 'https://orchestrator-xxx.run.app/api/analyze?ticker=NVDA'

# Load test (requires Apache Bench)
ab -n 100 -c 10 'https://orchestrator-xxx.run.app/api/analyze?ticker=TSLA'
```

### Test Different Tickers

Try these for varied results:
- **AAPL**: Large cap tech
- **GOOGL**: Growth stock
- **TSLA**: High volatility
- **JNJ**: Stable dividend
- **RIVN**: Small cap EV

## 🔄 Updates & CI/CD

### Manual Deployment

```bash
# Deploy new version
gcloud builds submit --config=deploy/cloudbuild.yaml

# Traffic is gradually shifted (5% → 100%)
# Automatic rollback if errors detected
```

### Automated CI/CD

Set up Cloud Build triggers:

```bash
# Connect GitHub repo
gcloud builds triggers create github \
  --repo-name=YOUR_REPO \
  --repo-owner=YOUR_GITHUB \
  --branch-pattern="^main$" \
  --build-config=deploy/cloudbuild.yaml
```

Now every push to `main` triggers deployment!

### Rollback

```bash
# View revisions
gcloud run revisions list --service=orchestrator --region=us-central1

# Rollback to specific revision
gcloud run services update-traffic orchestrator \
  --to-revisions=orchestrator-00042-abc=100 \
  --region=us-central1
```

## 🌍 Multi-Region Deployment

Deploy to multiple regions for:
- Lower latency worldwide
- Higher availability
- Disaster recovery

```bash
# Deploy to EU
gcloud builds submit \
  --config=deploy/cloudbuild.yaml \
  --substitutions=_REGION=europe-west1

# Deploy to Asia
gcloud builds submit \
  --config=deploy/cloudbuild.yaml \
  --substitutions=_REGION=asia-northeast1
```

Set up Cloud Load Balancer to route traffic to nearest region.

## 📱 Mobile & PWA

The UI is mobile-optimized and can be installed as a Progressive Web App:

**iOS:**
1. Open in Safari
2. Tap Share button
3. "Add to Home Screen"

**Android:**
1. Open in Chrome
2. Tap menu (⋮)
3. "Add to Home screen"

## 🎯 Vertex AI Native Integration

### Current A2A Implementation
Your deployment uses:
- A2A Protocol v0.3.0
- JSONRPC transport
- Agent cards for discovery
- Cloud Run hosting

### Migrate to Vertex AI Agent Builder

```bash
# Enable Vertex AI
gcloud services enable aiplatform.googleapis.com

# Create agent
gcloud ai agents create \
  --display-name="Stock Prediction System" \
  --config=deploy/vertex-agent-config.yaml \
  --region=us-central1
```

Benefits:
- Visual agent designer
- Pre-built templates
- Automatic scaling
- Native Google integration
- Advanced monitoring

## 🆘 Troubleshooting

### "Permission Denied"
```bash
# Ensure you're owner
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/owner"
```

### "Service Not Found"
```bash
# Check deployment
gcloud run services list --region=us-central1

# Redeploy if needed
./deploy/deploy.sh
```

### "Cold Start Timeout"
```bash
# Keep warm with Cloud Scheduler
gcloud scheduler jobs create http warm-services \
  --schedule="*/5 * * * *" \
  --uri="https://orchestrator-xxx.run.app/health"
```

### "Out of Memory"
```bash
# Increase memory
gcloud run services update orchestrator \
  --memory=4Gi \
  --region=us-central1
```

### "High Costs"
```bash
# Check current costs
gcloud billing accounts list
gcloud beta billing budgets list --billing-account=ACCOUNT_ID

# Reduce costs
# 1. Scale to zero when idle
# 2. Reduce max instances
# 3. Add caching
# 4. Use smaller machine types
```

## 📚 Additional Resources

### Documentation
- [Quick Start Guide](deploy/QUICKSTART.md)
- [Full Deployment Guide](deploy/DEPLOYMENT_GUIDE.md)
- [Cloud Deployment Summary](deploy/CLOUD_DEPLOYMENT_SUMMARY.md)
- [Architecture Details](ARCHITECTURE_SUMMARY.md)

### Google Cloud
- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- [Cloud Build Docs](https://cloud.google.com/build/docs)

### Community
- [Cloud Run Samples](https://github.com/GoogleCloudPlatform/cloud-run-samples)
- [Vertex AI Samples](https://github.com/GoogleCloudPlatform/vertex-ai-samples)
- [A2A Protocol](https://a2a-protocol.org/)

## 🎉 Success!

You now have a production-grade multi-agent AI system running on Google Cloud!

**Your URLs:**
```bash
# Frontend
echo "UI: https://$(gcloud config get-value project).uc.r.appspot.com"

# Backend
echo "API: $(gcloud run services describe orchestrator --region=us-central1 --format='value(status.url)')"
```

**Test it:**
```bash
# Via UI
open "https://$(gcloud config get-value project).uc.r.appspot.com?ticker=AAPL"

# Via API
curl "$(gcloud run services describe orchestrator --region=us-central1 --format='value(status.url)')/api/analyze?ticker=GOOGL"
```

**Share it:**
```
🎉 Just deployed a multi-agent AI stock analyzer to Google Cloud!

✅ 6 specialist agents with A2A protocol
✅ Real-time workflow visualization
✅ Auto-scaling production infrastructure
✅ Beautiful agentic UI

Try it: https://YOUR-PROJECT.uc.r.appspot.com?ticker=AAPL
```

---

**Need help? Check the [Deployment Guide](deploy/DEPLOYMENT_GUIDE.md) or [open an issue](https://github.com/your-repo/issues).**

**Built with ❤️ using Google Cloud, Vertex AI, Gemini, and the A2A Protocol**

