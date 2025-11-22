# ⚡ Quick Start - Deploy to Google Cloud in 15 Minutes

Get your multi-agent stock prediction system live on Google Cloud Platform.

## 🚀 One-Command Deployment

```bash
cd "Agent Capstone"

# Deploy everything
./deploy/deploy.sh && ./deploy/deploy-vertex-ui.sh
```

That's it! Your system will be live at `https://YOUR_PROJECT.uc.r.appspot.com`

## 📋 What You Need

1. **GCP Project** with billing enabled
2. **API Keys** (get them here):
   - Google AI: https://aistudio.google.com/apikey (FREE)
   - Polygon.io: https://polygon.io (you have this)
   - FRED: https://fred.stlouisfed.org (FREE, optional)
   - NewsAPI: https://newsapi.org (FREE, optional)

## 🎯 Step-by-Step

### 1. Setup gcloud CLI (5 min)

```bash
# Install (if not already)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Deploy Backend (10 min)

```bash
./deploy/deploy.sh
```

**You'll be asked for:**
- Project ID
- Region (default: us-central1)
- API Keys

**What gets deployed:**
- 6 Cloud Run services (agents)
- 1 Orchestrator service
- Secrets in Secret Manager
- Auto-scaling configuration

### 3. Deploy UI (3 min)

```bash
./deploy/deploy-vertex-ui.sh
```

**You'll be asked for:**
- Project ID (same as above)
- Region (same as above)

**What gets deployed:**
- App Engine service
- Beautiful dark-theme UI
- Real-time agent workflow viz

### 4. Test It! (2 min)

```bash
# Get your URL
gcloud app browse

# Or manually test
export ORCHESTRATOR_URL=$(gcloud run services describe orchestrator --region=us-central1 --format='value(status.url)')

# Health check
curl "$ORCHESTRATOR_URL/health"

# Analyze AAPL
curl "$ORCHESTRATOR_URL/api/analyze?ticker=AAPL"
```

## 🎨 UI Features

Your deployed UI includes:

- **Real-time Agent Workflow** - Watch agents work in parallel
- **Execution Timeline** - See exactly what happened when
- **Signal Visualization** - Colored bars for bullish/bearish signals
- **Confidence Gauges** - How sure is each agent?
- **Final Recommendation** - BUY/HOLD/SELL with rationale

## 📊 Try These Examples

Once deployed, try:

```bash
# Apple
https://YOUR_PROJECT.uc.r.appspot.com?ticker=AAPL

# Google
https://YOUR_PROJECT.uc.r.appspot.com?ticker=GOOGL

# NVIDIA
https://YOUR_PROJECT.uc.r.appspot.com?ticker=NVDA

# Tesla
https://YOUR_PROJECT.uc.r.appspot.com?ticker=TSLA
```

## 💰 Cost Estimate

**Free Tier (2M requests/month):**
- First 2M requests: FREE
- After that: ~$0.40 per 1M requests

**Typical Monthly Cost:**
- Light usage (< 100 analyses/day): **$5-10**
- Medium usage (< 1000 analyses/day): **$15-30**
- Heavy usage (> 1000 analyses/day): **$30-100**

**Cost breakdown:**
- Cloud Run: ~$5-20 (scales to zero)
- App Engine: ~$5-15 (F2 instance)
- Secret Manager: ~$0.50
- Container Registry: ~$0.50
- Cloud Build: ~$0.50 (one-time)

## 🔧 Customize

### Change Region

```bash
# Edit deploy scripts
sed -i 's/us-central1/europe-west1/g' deploy/*.sh
```

### Adjust Scaling

```bash
# More instances
gcloud run services update orchestrator \
  --max-instances=50 \
  --region=us-central1

# Keep warm (no cold starts)
gcloud run services update orchestrator \
  --min-instances=2 \
  --region=us-central1
```

### Update Agents

```bash
# Make code changes
vim agents/fundamental_analyst_server.py

# Redeploy
gcloud builds submit --config=deploy/cloudbuild.yaml
```

## 📈 Monitor

### View Logs

```bash
# Orchestrator logs
gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=orchestrator' --limit 50

# All services
gcloud logging tail 'resource.type=cloud_run_revision'
```

### Check Metrics

```bash
# Open monitoring dashboard
gcloud console cloud-monitoring
```

### Cost Tracking

```bash
# View billing
gcloud console billing
```

## 🛑 Stop/Delete

### Pause (Keep Everything, Stop Charges)

```bash
# Scale to zero
for service in orchestrator fundamental-agent technical-agent sentiment-agent macro-agent regulatory-agent predictor-agent; do
  gcloud run services update $service --min-instances=0 --max-instances=0 --region=us-central1
done

# Stop App Engine (can't truly stop, but disable)
gcloud app versions delete default
```

### Delete Everything

```bash
# Delete Cloud Run
for service in orchestrator fundamental-agent technical-agent sentiment-agent macro-agent regulatory-agent predictor-agent; do
  gcloud run services delete $service --region=us-central1 --quiet
done

# Delete App Engine (requires confirmation)
gcloud app services delete default --quiet

# Clean up images
gcloud container images list --repository=gcr.io/YOUR_PROJECT_ID
gcloud container images delete gcr.io/YOUR_PROJECT_ID/stock-agent-base:latest --quiet
```

## 🆘 Troubleshooting

### "Permission Denied"
```bash
# Add yourself as owner
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:YOUR_EMAIL@gmail.com" \
  --role="roles/owner"
```

### "Service Not Found"
```bash
# Check if deployed
gcloud run services list --region=us-central1

# Redeploy
./deploy/deploy.sh
```

### "Timeout Error"
```bash
# Increase timeout
gcloud run services update orchestrator \
  --timeout=600 \
  --region=us-central1
```

### "Out of Memory"
```bash
# Increase memory
gcloud run services update orchestrator \
  --memory=4Gi \
  --region=us-central1
```

## 🎓 Learn More

- [Full Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Architecture Details](../ARCHITECTURE_SUMMARY.md)
- [Agent Documentation](../AGENT_DEEP_DIVE_FEATURES.md)
- [GCP Documentation](https://cloud.google.com/run/docs)

## ✨ Next Steps

After deployment:

1. **Add Authentication** - Restrict access to authorized users
2. **Set Up Monitoring** - Create alerts for errors and costs
3. **Enable Caching** - Speed up repeated queries
4. **Add Rate Limiting** - Protect against abuse
5. **Custom Domain** - Map to your own domain
6. **CI/CD Pipeline** - Automate deployments

## 🎉 You're Live!

Your multi-agent stock prediction system is now running on Google Cloud Platform!

**Share your deployment:**
```bash
echo "Check out my AI stock analyzer: $(gcloud app browse --no-launch-browser 2>&1 | grep https)"
```

**Need help?** Check the [Deployment Guide](DEPLOYMENT_GUIDE.md) or [open an issue](https://github.com/your-repo/issues).

---

**Built with ❤️ using Google ADK, Vertex AI, and Cloud Run**

