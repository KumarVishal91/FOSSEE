# Deployment Checklist

## Before Deploying

### Backend (Render)

- [ ] Push latest code to GitHub
- [ ] Verify `render.yaml` configuration
- [ ] Check `requirements.txt` is up to date
- [ ] Ensure migrations are included

### Frontend (Vercel)

- [ ] Verify `vercel.json` configuration
- [ ] Check `package.json` build scripts
- [ ] Test production build locally: `npm run build`

## Deployment Steps

### 1. Deploy Backend First

- [ ] Go to [Render Dashboard](https://dashboard.render.com/)
- [ ] Deploy using Blueprint (render.yaml)
- [ ] Set environment variables:
  - [ ] `DJANGO_SECRET_KEY` (generate)
  - [ ] `DJANGO_DEBUG=false`
  - [ ] `DJANGO_ALLOWED_HOSTS` (your-app.onrender.com)
  - [ ] `DJANGO_CORS_ORIGINS` (placeholder, update after frontend)
  - [ ] `DJANGO_CSRF_TRUSTED_ORIGINS` (placeholder, update after frontend)
- [ ] Wait for successful deployment
- [ ] **Copy backend URL:** `https://____________.onrender.com`
- [ ] Test admin panel: `https://your-app.onrender.com/admin/`
- [ ] Login with: admin / admin123

### 2. Deploy Frontend

- [ ] Go to [Vercel](https://vercel.com/new)
- [ ] Import GitHub repository
- [ ] Set root directory: `chemical_visualizer/web`
- [ ] Add environment variable:
  ```
  REACT_APP_API_URL=https://your-backend.onrender.com/api
  ```
  (Use the URL from step 1)
- [ ] Deploy
- [ ] **Copy frontend URL:** `https://____________.vercel.app`
- [ ] Test the application

### 3. Update CORS Settings

- [ ] Go back to Render dashboard
- [ ] Update environment variables:
  - [ ] `DJANGO_CORS_ORIGINS=https://your-frontend.vercel.app`
  - [ ] `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app`
- [ ] Click "Manual Deploy" to redeploy with new settings

### 4. Final Testing

- [ ] Open frontend: `https://your-frontend.vercel.app`
- [ ] Test login with admin/admin123
- [ ] Upload sample CSV file
- [ ] Verify charts display correctly
- [ ] Download PDF report
- [ ] Check history functionality
- [ ] Test on mobile device

## Post-Deployment

### Security

- [ ] Change default admin password
- [ ] Keep `DJANGO_SECRET_KEY` secure
- [ ] Verify `DJANGO_DEBUG=false` in production

### Monitoring

- [ ] Check Render logs for errors
- [ ] Monitor Vercel deployment logs
- [ ] Set up uptime monitoring (optional)

### Documentation

- [ ] Update README with live URLs
- [ ] Document any custom domain setup
- [ ] Share access credentials with team

## URLs to Save

```
Backend:  https://_________________.onrender.com
Frontend: https://_________________.vercel.app
GitHub:   https://github.com/KumarVishal91/FOSSEE
```

## Troubleshooting

### CORS Errors
- Verify frontend URL in `DJANGO_CORS_ORIGINS`
- Check `DJANGO_CSRF_TRUSTED_ORIGINS`
- Ensure no trailing slashes

### 500 Errors
- Check Render logs
- Verify environment variables
- Ensure migrations ran successfully

### Static Files Not Loading
- Check `STATIC_ROOT` in settings
- Verify `collectstatic` in build command

## Redeployment

### Backend
- Push to main branch (auto-deploys)
- Or click "Manual Deploy" in Render

### Frontend
- Push to main branch (auto-deploys)
- Or use Vercel CLI: `vercel --prod`

---

**Need help?** See detailed guides:
- [Backend: DEPLOY_RENDER.md](backend/DEPLOY_RENDER.md)
- [Frontend: web/DEPLOY_VERCEL.md](web/DEPLOY_VERCEL.md)
