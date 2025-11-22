# 🚀 Auto-Deploy Setup Instructions

## What You Need to Provide

Before running the setup, have these ready:

1. **Google Cloud Project ID** - Your GCP project
2. **GOOGLE_API_KEY** - Your Google API key (for Gemini)
3. **POLYGON_API_KEY** (optional) - If you use Polygon.io
4. **GitHub Repository** (optional) - For automatic deployment on push

## Quick Setup (One-Time)

Run this **once** to configure everything:

```bash
bash scripts/auto_deploy_setup.sh
```

This script will:
- ✅ Authenticate and set your project
- ✅ Enable all required APIs
- ✅ Store secrets securely
- ✅ Deploy agents (if not already deployed)
- ✅ Setup Cloud Build triggers (optional)
- ✅ Create auto-deploy script

## What Happens Automatically

### Option 1: Manual Deploy
After setup, you can deploy anytime with:
```bash
bash scripts/auto_deploy.sh
```

### Option 2: Auto-Deploy on Git Push
If you set up the GitHub trigger:
- Push to your repository → Cloud Build automatically deploys
- No manual steps needed

## Setup Process

### Step 1: Run Setup Script
```bash
bash scripts/auto_deploy_setup.sh
```

You'll be prompted for:
- Project ID (or use current)
- Region (default: us-central1)
- GOOGLE_API_KEY (stored in Secret Manager)
- POLYGON_API_KEY (optional)
- GitHub repo (optional, for auto-deploy)

### Step 2: Wait for Setup
The script will:
1. Enable all required Google Cloud APIs
2. Store your API keys in Secret Manager
3. Grant Cloud Build access to secrets
4. Deploy agents (if needed)
5. Create configuration file (`.deploy_config`)

### Step 3: Done!
- Manual deploy: `bash scripts/auto_deploy.sh`
- Auto-deploy: Push to GitHub (if trigger set up)

## What Gets Deployed

1. **Agent Registry** - Service for discovering external agents
2. **Chatbot** - Function calling chatbot with Gemini API

Both services:
- Auto-scale based on traffic
- Use secrets from Secret Manager
- Connect to your A2A agents
- Support external agent discovery

## Configuration File

After setup, `.deploy_config` is created:
```
PROJECT_ID=your-project-id
REGION=us-central1
```

**Don't commit this file** - it's in `.gitignore`

## Troubleshooting

### "Secrets not found"
```bash
# Manually create secret
echo -n "your-api-key" | gcloud secrets create GOOGLE_API_KEY --data-file=-
```

### "Agents not deployed"
```bash
# Deploy agents first
gcloud builds submit --config=deploy/cloudbuild.yaml
```

### "Permission denied"
```bash
# Grant Cloud Build access
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Manual Override

If auto-deploy fails, deploy manually:

```bash
# Load config
source .deploy_config

# Deploy
gcloud builds submit \
  --config=deploy/cloudbuild-chatbot.yaml \
  --substitutions="_REGION=$REGION" \
  --project=$PROJECT_ID
```

## Check Deployment Status

```bash
# Check services
gcloud run services list --region=us-central1

# Check logs
gcloud logging read "resource.type=cloud_run_revision" --limit=10

# Test chatbot
CHATBOT_URL=$(gcloud run services describe stock-chatbot --region=us-central1 --format='value(status.url)')
curl -X POST "$CHATBOT_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze AAPL fundamentals"}'
```

## Next Steps After Setup

1. **Test deployment**: Run `bash scripts/auto_deploy.sh`
2. **Subscribe to external agents**: Use registry API
3. **Monitor**: Check Cloud Logging
4. **Scale**: Adjust min/max instances in Cloud Run

---

**Once setup is complete, you can step away - deployments will happen automatically!** 🎉

