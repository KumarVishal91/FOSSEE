# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop)

This project provides a Django REST backend with a React web UI and a PyQt5 desktop client. It supports CSV upload, analytics, charting, history (last 5 datasets), and PDF report generation.

## Features
- CSV upload (Web + Desktop)
- Summary analytics (total count, averages, type distribution)
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
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

> Use the credentials you create for both the web and desktop apps.

## Web App Setup
```bash
cd web
npm install
npm start
```

Optional: set API URL
```bash
set REACT_APP_API_URL=http://127.0.0.1:8000/api
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
