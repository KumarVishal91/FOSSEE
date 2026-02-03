# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project provides a Django REST backend with a React web UI and a PyQt5 desktop client. It supports CSV upload, analytics, charting, history (last 5 datasets), and PDF report generation.

## Features
- CSV upload (Web + Desktop)
- Summary analytics (total, invalid rows, min/max/averages, type distribution)
- Charts (Chart.js on Web, Matplotlib on Desktop)
- History of last 5 uploads
- PDF report generation
- Basic authentication

## Project Structure
- `backend/` – Django + DRF API
- `web/` – React web application
- `web/desktop/` – PyQt5 desktop client
- `sample_equipment_data.csv` – sample data

### Local Development Setup

## Backend Setup

### Option 1: Quick Setup (Default Admin)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_default_user
python manage.py runserver
```

> Default credentials: **username:** `admin` | **password:** `admin123`

### Option 2: Custom Admin Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

> Use the credentials you create for both the web and desktop apps.

### Environment Variables (Optional)
Copy `.env.example` to `.env` and configure:
```bash
copy .env.example .env
```

## Web App Setup
```bash
cd web
npm install
npm start
```

Optional: Configure API URL by copying `.env.example` to `.env`
```bash
copy .env.example .env
```

## Desktop App Setup
```bash
cd web\desktop
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## API Endpoints
- `POST /api/upload/` – Upload CSV
- `GET /api/history/` – Last 5 datasets
- `GET /api/datasets/latest/` – Latest dataset
- `GET /api/datasets/<id>/` – Dataset detail
- `GET /api/report/<id>/` – PDF report

## Notes
- The backend uses HTTP Basic Authentication.
- CORS is enabled for `http://localhost:3000`.
- CSV required columns: Equipment Name, Type, Flowrate, Pressure, Temperature.
- Run tests: `cd backend && python manage.py test`

## Deployment

### 🚀 Quick Deploy (10 minutes)

See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for the fastest deployment path.

**TL;DR:**
1. Deploy backend to Render: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/KumarVishal91/FOSSEE)
2. Deploy frontend to Vercel: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/KumarVishal91/FOSSEE/tree/main/chemical_visualizer/web)
3. Update CORS settings

### Complete Deployment Guide

**Frontend (Vercel)** + **Backend (Render)**

#### Step 1: Deploy Backend to Render

See detailed guide: [backend/DEPLOY_RENDER.md](backend/DEPLOY_RENDER.md)

**Quick steps:**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Blueprint**
3. Connect your GitHub repo
4. Deploy the `render.yaml` configuration
5. Copy your backend URL: `https://your-app.onrender.com`

**Set these environment variables in Render:**
- `DJANGO_SECRET_KEY` - Auto-generate
- `DJANGO_DEBUG` = `false`
- `DJANGO_ALLOWED_HOSTS` = `your-app.onrender.com`
- `DJANGO_CORS_ORIGINS` = `https://your-frontend.vercel.app` (update after frontend deploy)
- `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://your-frontend.vercel.app` (update after frontend deploy)

#### Step 2: Deploy Frontend to Vercel

See detailed guide: [web/DEPLOY_VERCEL.md](web/DEPLOY_VERCEL.md)

**Quick steps:**
1. Go to [Vercel](https://vercel.com/new)
2. Import your GitHub repository
3. Set root directory: `chemical_visualizer/web`
4. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com/api
   ```
5. Deploy

#### Step 3: Update CORS Settings

After both are deployed:
1. Go back to Render dashboard
2. Update environment variables with your actual Vercel URL
3. Redeploy backend

### Deployment Architecture

```
┌─────────────────────┐
│   Vercel (Frontend) │
│   React + Chart.js  │
└──────────┬──────────┘
           │ HTTPS
           ↓
┌─────────────────────┐
│   Render (Backend)  │
│  Django + REST API  │
│   SQLite Database   │
└─────────────────────┘
```

### Local Development Setup

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Structure

```
chemical_visualizer/
├── backend/              # Django REST API
│   ├── api/             # Main API app
│   ├── backend/         # Django settings
│   ├── media/           # Uploaded CSV files
│   └── requirements.txt
├── web/                 # React web app
│   ├── desktop/         # PyQt5 desktop app
│   ├── public/
│   ├── src/
│   └── package.json
├── sample_equipment_data.csv
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```
