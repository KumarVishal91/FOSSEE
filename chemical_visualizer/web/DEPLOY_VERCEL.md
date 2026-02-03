# Vercel Deployment Guide

## Quick Deploy

1. Click the button below or go to [vercel.com](https://vercel.com)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/KumarVishal91/FOSSEE/tree/main/chemical_visualizer/web)

## Manual Deployment

### 1. Install Vercel CLI (optional)
```bash
npm install -g vercel
```

### 2. Configure Environment Variables

In your Vercel project settings, add:

```
REACT_APP_API_URL=https://your-backend.onrender.com/api
```

### 3. Deploy via CLI
```bash
cd web
vercel --prod
```

### 4. Deploy via Git Integration

1. Push your code to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Set root directory to `chemical_visualizer/web`
5. Add environment variable `REACT_APP_API_URL`
6. Deploy

## Build Settings

- **Framework Preset:** Create React App
- **Root Directory:** `chemical_visualizer/web`
- **Build Command:** `npm run build`
- **Output Directory:** `build`
- **Install Command:** `npm install`

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `REACT_APP_API_URL` | `https://your-backend.onrender.com/api` | Backend API URL |

## Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Important Notes

- After deploying backend to Render, update `REACT_APP_API_URL` with your Render backend URL
- Rebuild the project after changing environment variables
- The frontend will automatically redeploy on every push to main branch (if using Git integration)
