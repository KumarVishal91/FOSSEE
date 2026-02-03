# Render Deployment Guide

## Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/KumarVishal91/FOSSEE)

## Manual Deployment

### 1. Prerequisites
- GitHub account
- Render account ([sign up](https://render.com))

### 2. Deploy Backend

#### Option A: Using Blueprint (render.yaml)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Blueprint**
3. Connect your GitHub repository: `https://github.com/KumarVishal91/FOSSEE`
4. Render will detect the `render.yaml` file
5. Review the configuration
6. Click **Apply** to deploy

#### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `chemical-visualizer-backend`
   - **Root Directory:** `chemical_visualizer/backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py create_default_user`
   - **Start Command:** `gunicorn backend.wsgi:application`

### 3. Configure Environment Variables

Add these in the Render dashboard under "Environment":

| Variable | Value | Notes |
|----------|-------|-------|
| `DJANGO_SECRET_KEY` | (auto-generated) | Click "Generate" |
| `DJANGO_DEBUG` | `false` | Production setting |
| `DJANGO_ALLOWED_HOSTS` | `your-app.onrender.com` | Your Render URL |
| `DJANGO_CORS_ORIGINS` | `https://your-app.vercel.app` | Your Vercel frontend URL |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://your-app.vercel.app` | Your Vercel frontend URL |

### 4. Deploy & Get Backend URL

1. Wait for the build to complete
2. Your backend will be available at: `https://your-app.onrender.com`
3. Copy this URL - you'll need it for the frontend

### 5. Test Backend

Visit: `https://your-app.onrender.com/admin/`

Login with default credentials:
- **Username:** `admin`
- **Password:** `admin123`

### 6. Update Frontend

After backend deployment, update your Vercel frontend:

1. Go to Vercel project settings
2. Update environment variable:
   ```
   REACT_APP_API_URL=https://your-app.onrender.com/api
   ```
3. Redeploy frontend

## Post-Deployment

### Update CORS Settings

After deploying frontend to Vercel:

1. Go to Render dashboard
2. Navigate to your service → Environment
3. Update:
   - `DJANGO_CORS_ORIGINS` = `https://your-frontend.vercel.app`
   - `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://your-frontend.vercel.app`
   - `DJANGO_ALLOWED_HOSTS` = `your-backend.onrender.com`
4. Save and redeploy

### Database Persistence

Render uses persistent disk for SQLite:
- Free tier includes 1GB disk
- Database persists across deployments
- Last 5 datasets are stored

### Custom Domain (Optional)

1. Go to service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed

## Monitoring

- **Logs:** Available in Render dashboard
- **Metrics:** CPU, memory, request metrics
- **Auto-deploy:** Enabled on push to main branch

## Troubleshooting

### Build Fails
- Check `requirements.txt` is in `chemical_visualizer/backend/`
- Verify Python version in `runtime.txt`

### CORS Errors
- Ensure frontend URL is in `DJANGO_CORS_ORIGINS`
- Check `DJANGO_CSRF_TRUSTED_ORIGINS` includes frontend URL

### Migration Issues
- Migrations run automatically on each deploy
- Check logs for migration errors

## Cost

- **Free Tier:** Available
- **Paid Plans:** Starting at $7/month for better performance
- **Database:** Included in web service

## Important Notes

1. Free tier services may spin down after inactivity (50-60 seconds to wake up)
2. Change default admin password after deployment
3. Set `DJANGO_DEBUG=false` in production
4. Keep `DJANGO_SECRET_KEY` secret and unique
