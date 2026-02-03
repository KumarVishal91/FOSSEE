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

## Deployment (Optional)

### Backend Deployment (Render/Heroku)
The project includes `Procfile` and `runtime.txt` for easy deployment to Render or Heroku.

### Frontend Deployment (Vercel/Netlify)
Build the React app and deploy the `build` folder:
```bash
cd web
npm run build
```

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
