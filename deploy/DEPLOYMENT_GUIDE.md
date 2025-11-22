# 🚀 Google Cloud Deployment Guide

Complete guide to deploying the Stock Prediction Multi-Agent System on Google Cloud Platform with Vertex AI.

## 📋 Prerequisites

1. **Google Cloud Account**
   - Active GCP project
   - Billing enabled
   - Owner or Editor permissions

2. **Local Tools**
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   
   # Initialize gcloud
   gcloud init
   gcloud auth login
   ```

3. **API Keys**
   - Google AI (Gemini): https://aistudio.google.com/apikey
   - Polygon.io: https://polygon.io/dashboard/api-keys
   - FRED (optional): https://fred.stlouisfed.org/docs/api/api_key.html
   - NewsAPI (optional): https://newsapi.org/register

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              App Engine (UI)                        │
│         https://PROJECT.uc.r.appspot.com            │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│         Cloud Run (Orchestrator)                    │
│    https://orchestrator-xxx.run.app                 │
└────────┬────────────────────────────────────────────┘
         │
         ├──► Cloud Run: fundamental-agent
         ├──► Cloud Run: technical-agent
         ├──► Cloud Run: sentiment-agent
         ├──► Cloud Run: macro-agent
         ├──► Cloud Run: regulatory-agent
         └──► Cloud Run: predictor-agent
              │
              ▼
      ┌──────────────────┐
      │ Secret Manager   │
      │ - API Keys       │
      │ - Credentials    │
      └──────────────────┘
```

## 📦 Step 1: Deploy Backend Agents

```bash
cd "Agent Capstone"

# Run deployment script
./deploy/deploy.sh
```

**What happens:**
1. Enables required GCP APIs
2. Creates secrets in Secret Manager
3. Builds Docker containers via Cloud Build
4. Deploys 6 agent services to Cloud Run
5. Deploys orchestrator with agent URLs
6. Configures auto-scaling (0-10 instances)

**Time:** ~15-20 minutes

**Cost:** 
- Cloud Build: ~$0.50
- Cloud Run: ~$5-20/month (depends on usage)
- Container Registry: ~$0.50/month

## 🎨 Step 2: Deploy Frontend UI

```bash
# Deploy to App Engine
./deploy/deploy-vertex-ui.sh
```

**What happens:**
1. Gets orchestrator URL from Cloud Run
2. Updates UI configuration
3. Deploys to App Engine
4. Returns public URL

**Time:** ~5-10 minutes

**Cost:**
- App Engine: ~$5-15/month (F2 instance)

## ✅ Step 3: Verify Deployment

```bash
# Test orchestrator API
ORCHESTRATOR_URL=$(gcloud run services describe orchestrator --region=us-central1 --format='value(status.url)')
curl "$ORCHESTRATOR_URL/health"

# Test analysis
curl "$ORCHESTRATOR_URL/api/analyze?ticker=AAPL"

# Open UI
gcloud app browse
```

## 🔧 Configuration

### Environment Variables

Set via Cloud Run:
```bash
gcloud run services update orchestrator \
  --update-env-vars="LOG_LEVEL=INFO,TIMEOUT=300"
```

### Scaling

Adjust auto-scaling:
```bash
gcloud run services update fundamental-agent \
  --min-instances=1 \
  --max-instances=20 \
  --region=us-central1
```

### Memory/CPU

Update resources:
```bash
gcloud run services update orchestrator \
  --memory=4Gi \
  --cpu=4 \
  --region=us-central1
```

## 📊 Monitoring

### View Logs

```bash
# Orchestrator logs
gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=orchestrator' \
  --limit 50 \
  --format json

# All agents
gcloud logging read 'resource.type=cloud_run_revision' \
  --filter='resource.labels.service_name:agent' \
  --limit 100
```

### Metrics Dashboard

```bash
# Open Cloud Console
gcloud console cloud-monitoring
```

Navigate to: **Monitoring → Dashboards**

Key metrics to track:
- Request count
- Latency (p50, p95, p99)
- Error rate
- Instance count
- API costs

### Alerts

Create alerts for:
- Error rate > 5%
- Latency > 10s
- Daily cost > $10

## 🔐 Security

### Add Authentication

For production, enable IAM authentication:

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

### API Key Rotation

```bash
# Update secret
echo -n "new_api_key" | gcloud secrets versions add GOOGLE_API_KEY --data-file=-

# Restart services
gcloud run services update orchestrator --region=us-central1
```

### Rate Limiting

Add Cloud Armor for DDoS protection:
```bash
gcloud compute security-policies create rate-limit-policy \
  --description="Rate limit for stock analysis"

gcloud compute security-policies rules create 1000 \
  --security-policy=rate-limit-policy \
  --expression="true" \
  --action="rate-based-ban" \
  --rate-limit-threshold-count=100 \
  --rate-limit-threshold-interval-sec=60
```

## 💰 Cost Optimization

### Free Tier Usage

Cloud Run free tier (per month):
- 2 million requests
- 360,000 GB-seconds
- 180,000 vCPU-seconds

Strategy to stay in free tier:
```bash
# Set min instances to 0 (scale to zero)
for service in fundamental-agent technical-agent sentiment-agent macro-agent regulatory-agent predictor-agent; do
  gcloud run services update $service \
    --min-instances=0 \
    --region=us-central1
done

# Keep orchestrator warm
gcloud run services update orchestrator \
  --min-instances=1 \
  --region=us-central1
```

### Budget Alerts

```bash
# Create budget
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT \
  --display-name="Stock Analysis Budget" \
  --budget-amount=50USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
```

## 🔄 Updates & Maintenance

### Deploy New Version

```bash
# Build and deploy
gcloud builds submit --config=deploy/cloudbuild.yaml

# Or deploy specific agent
gcloud run deploy fundamental-agent \
  --image=gcr.io/PROJECT_ID/stock-agent-base:latest \
  --region=us-central1
```

### Rollback

```bash
# List revisions
gcloud run revisions list --service=orchestrator --region=us-central1

# Rollback
gcloud run services update-traffic orchestrator \
  --to-revisions=orchestrator-00001-abc=100 \
  --region=us-central1
```

### Delete Everything

```bash
# Delete Cloud Run services
gcloud run services delete orchestrator --region=us-central1
for service in fundamental-agent technical-agent sentiment-agent macro-agent regulatory-agent predictor-agent; do
  gcloud run services delete $service --region=us-central1 --quiet
done

# Delete App Engine (requires manual confirmation)
gcloud app versions delete --service=default

# Delete secrets
gcloud secrets delete GOOGLE_API_KEY
gcloud secrets delete POLYGON_API_KEY
```

## 🧪 Testing

### Load Testing

```bash
# Install Apache Bench
brew install httpd  # macOS

# Test
ab -n 100 -c 10 "$ORCHESTRATOR_URL/api/analyze?ticker=AAPL"
```

### CI/CD Pipeline

See `deploy/cloudbuild.yaml` for automated testing and deployment.

## 🎯 Vertex AI Integration

### Enable Vertex AI Agent Builder

```bash
# Enable API
gcloud services enable aiplatform.googleapis.com

# Upload agent config
gcloud ai agents create \
  --display-name="Stock Prediction System" \
  --config=deploy/vertex-agent-config.yaml \
  --region=us-central1
```

### Use Vertex AI Console

1. Go to: https://console.cloud.google.com/vertex-ai/agents
2. Click "Create Agent"
3. Upload `deploy/vertex-agent-config.yaml`
4. Test in the playground
5. Deploy to endpoint

## 📝 Best Practices

1. **Use Cloud Scheduler** for warming cold instances:
   ```bash
   gcloud scheduler jobs create http warm-orchestrator \
     --schedule="*/5 * * * *" \
     --uri="$ORCHESTRATOR_URL/health" \
     --http-method=GET
   ```

2. **Enable Cloud Trace** for detailed latency analysis

3. **Set up Cloud Error Reporting** for automatic error tracking

4. **Use Cloud CDN** for caching frequent queries

5. **Implement request deduplication** for identical concurrent requests

## 🆘 Troubleshooting

### Cold Start Issues
- Increase min instances to 1
- Use Cloud Scheduler to keep warm
- Optimize Docker image size

### Timeout Errors
- Increase timeout: `--timeout=600`
- Check agent response times
- Add retry logic

### Out of Memory
- Increase memory: `--memory=4Gi`
- Check for memory leaks
- Monitor with Cloud Trace

### API Rate Limits
- Implement caching
- Add exponential backoff
- Monitor quota usage

## 📞 Support

- GCP Status: https://status.cloud.google.com
- Cloud Run Docs: https://cloud.google.com/run/docs
- Vertex AI Docs: https://cloud.google.com/vertex-ai/docs

## 🎉 Success Metrics

After deployment, you should see:
- ✅ All 6 agents responding to health checks
- ✅ Orchestrator returning analysis in < 10s
- ✅ UI accessible via App Engine URL
- ✅ Logs flowing to Cloud Logging
- ✅ Costs within budget
- ✅ 99.9%+ uptime

**Your multi-agent system is now live on Google Cloud! 🚀**

