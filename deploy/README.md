# 🚀 Deployment Files

This directory contains everything needed to deploy the Stock Prediction Multi-Agent System to Google Cloud Platform.

## 📁 Files Overview

```
deploy/
├── deploy.sh                    # Main deployment script
├── deploy-vertex-ui.sh          # UI deployment script
├── test-deployment.sh           # Test deployed services
├── cloudbuild.yaml              # Cloud Build configuration
├── Dockerfile.agent             # Agent container image
├── Dockerfile.orchestrator      # Orchestrator container image
├── vertex-agent-config.yaml     # Vertex AI configuration
├── vertex-ui/                   # UI application
│   ├── index.html              # Agentic UI with workflow viz
│   ├── app.yaml                # App Engine config
│   ├── main.py                 # Proxy server
│   └── requirements.txt        # Python deps
├── QUICKSTART.md               # 15-minute quick start
└── DEPLOYMENT_GUIDE.md         # Complete deployment guide
```

## 🎯 Quick Commands

### Deploy Everything
```bash
# From project root
./deploy/deploy.sh && ./deploy/deploy-vertex-ui.sh
```

### Test Deployment
```bash
./deploy/test-deployment.sh
```

### View Logs
```bash
gcloud logging tail 'resource.type=cloud_run_revision'
```

### Update Services
```bash
gcloud builds submit --config=deploy/cloudbuild.yaml
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 15 minutes
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide
- **[vertex-agent-config.yaml](vertex-agent-config.yaml)** - Vertex AI configuration

## 🏗️ Architecture

The deployment creates:

1. **6 Cloud Run Services** (Agents)
   - fundamental-agent
   - technical-agent
   - sentiment-agent
   - macro-agent
   - regulatory-agent
   - predictor-agent

2. **1 Cloud Run Service** (Orchestrator)
   - Coordinates all agents
   - Provides REST API

3. **1 App Engine Service** (UI)
   - Beautiful dark-theme interface
   - Real-time workflow visualization

4. **Secret Manager**
   - Stores API keys securely

5. **Container Registry**
   - Stores Docker images

## 💰 Cost Estimate

**Monthly costs:**
- Light usage (< 100 analyses/day): $5-10
- Medium usage (< 1000 analyses/day): $15-30
- Heavy usage (> 1000 analyses/day): $30-100

**Free tier:**
- 2M Cloud Run requests/month
- 360K GB-seconds compute
- 180K vCPU-seconds

## 🔐 Security

All API keys are stored in Secret Manager and never exposed in:
- Container images
- Environment variables (visible in console)
- Logs
- Source code

## 🎨 UI Features

The deployed UI includes:

- **Real-time Agent Workflow** - See agents work in parallel
- **Execution Timeline** - Track what happened when
- **Signal Visualization** - Bullish/bearish indicators
- **Confidence Gauges** - Agent certainty levels
- **Final Recommendations** - BUY/HOLD/SELL with reasoning

## 📊 Monitoring

**View metrics:**
```bash
# Open Cloud Console
gcloud console cloud-monitoring
```

**Key metrics:**
- Request count
- Latency (p50, p95, p99)
- Error rate
- Instance count

## 🔄 Updates

**Deploy new version:**
```bash
# Make code changes
vim ../agents/fundamental_analyst_server.py

# Rebuild and deploy
gcloud builds submit --config=deploy/cloudbuild.yaml
```

**Rollback:**
```bash
# List revisions
gcloud run revisions list --service=orchestrator

# Rollback
gcloud run services update-traffic orchestrator \
  --to-revisions=REVISION_NAME=100
```

## 🛑 Cleanup

**Delete everything:**
```bash
# Delete Cloud Run services
for service in orchestrator fundamental-agent technical-agent sentiment-agent macro-agent regulatory-agent predictor-agent; do
  gcloud run services delete $service --region=us-central1 --quiet
done

# Delete App Engine
gcloud app versions delete default --quiet

# Delete images
gcloud container images delete gcr.io/PROJECT_ID/stock-agent-base:latest --quiet
gcloud container images delete gcr.io/PROJECT_ID/stock-orchestrator:latest --quiet

# Delete secrets
gcloud secrets delete GOOGLE_API_KEY --quiet
gcloud secrets delete POLYGON_API_KEY --quiet
```

## 🆘 Troubleshooting

**Common issues:**

1. **Permission errors** - Ensure billing is enabled
2. **Timeout errors** - Increase `--timeout=600`
3. **Memory errors** - Increase `--memory=4Gi`
4. **Cold starts** - Set `--min-instances=1`

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed troubleshooting.

## 📞 Support

- **GCP Status**: https://status.cloud.google.com
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Vertex AI Docs**: https://cloud.google.com/vertex-ai/docs

## ✨ Features

After deployment, you get:

- ✅ Fully managed, auto-scaling services
- ✅ HTTPS endpoints with Google-managed certificates
- ✅ Zero-downtime deployments
- ✅ Automatic health checks
- ✅ Built-in monitoring and logging
- ✅ Pay only for what you use
- ✅ Scale to zero when idle

## 🎓 Learn More

- [A2A Protocol](https://a2a-protocol.org/)
- [Google ADK](https://google.github.io/adk-docs/)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)

---

**Ready to deploy? Start with [QUICKSTART.md](QUICKSTART.md)!**

