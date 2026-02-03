## Quick Start - Deployment

### 1. Deploy Backend to Render (5 minutes)

1. **Go to Render:** https://dashboard.render.com/
2. **Click:** New → Blueprint
3. **Connect:** Your GitHub repo (KumarVishal91/FOSSEE)
4. **Render will auto-detect** `render.yaml`
5. **Click Apply** and wait for deployment
6. **Save your backend URL:** `https://your-app.onrender.com`

### 2. Deploy Frontend to Vercel (3 minutes)

1. **Go to Vercel:** https://vercel.com/new
2. **Import** your GitHub repo
3. **Set root directory:** `chemical_visualizer/web`
4. **Add environment variable:**
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-backend.onrender.com/api` (from step 1)
5. **Click Deploy**
6. **Save your frontend URL:** `https://your-app.vercel.app`

### 3. Update CORS (2 minutes)

1. **Go back to Render** dashboard
2. **Open your service** → Environment
3. **Update these variables:**
   - `DJANGO_CORS_ORIGINS` = `https://your-frontend.vercel.app`
   - `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://your-frontend.vercel.app`
   - `DJANGO_ALLOWED_HOSTS` = `your-app.onrender.com`
4. **Click:** Manual Deploy → Deploy latest commit

### 4. Test Your App

Visit: `https://your-frontend.vercel.app`

Login with:
- Username: `admin`
- Password: `admin123`

**🎉 Done! Your app is live!**

---

**Need detailed instructions?** See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
