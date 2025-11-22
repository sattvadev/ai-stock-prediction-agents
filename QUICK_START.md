# ⚡ Quick Start - Auto Deploy

## One Command Setup

Run this **once** before you step away:

```bash
bash scripts/auto_deploy_setup.sh
```

## What You Need

1. **Google Cloud Project ID**
2. **GOOGLE_API_KEY** (for Gemini)
3. **POLYGON_API_KEY** (optional)

## What Happens

✅ Sets up your project  
✅ Stores secrets securely  
✅ Deploys agents (if needed)  
✅ Creates auto-deploy script  
✅ Optionally sets up GitHub auto-deploy  

## After Setup

### Manual Deploy Anytime:
```bash
bash scripts/auto_deploy.sh
```

### Auto-Deploy on Git Push:
If you set up GitHub trigger, just push:
```bash
git push origin main
# Cloud Build automatically deploys!
```

## That's It!

Once setup is done, you can step away. Deployments happen automatically on git push (if configured) or run `bash scripts/auto_deploy.sh` anytime.

See `AUTO_DEPLOY_INSTRUCTIONS.md` for details.

