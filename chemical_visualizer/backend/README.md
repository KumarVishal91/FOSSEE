# Chemical Equipment Parameter Visualizer - Backend API

Django REST Framework backend for chemical equipment data analysis.

## Features
- CSV file upload and parsing
- Data validation and cleaning
- Summary statistics (totals, averages, min/max, distributions)
- Last 5 datasets history
- PDF report generation
- Basic authentication
- RESTful API endpoints

## Tech Stack
- Django 6.0
- Django REST Framework
- Pandas (data processing)
- ReportLab (PDF generation)
- SQLite database

## Setup

### Quick Setup (Default Admin)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_default_user
python manage.py runserver
```

Default credentials: **username:** `admin` | **password:** `admin123`

### Custom Admin Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/upload/` | Upload CSV file | Yes |
| GET | `/api/history/` | Get last 5 datasets | Yes |
| GET | `/api/datasets/latest/` | Get latest dataset | Yes |
| GET | `/api/datasets/<id>/` | Get dataset by ID | Yes |
| GET | `/api/report/<id>/` | Download PDF report | Yes |

## CSV Format

Required columns:
- Equipment Name
- Type
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120.5,3.2,65
Reactor 1,Reactor,80.0,5.8,120
```

## Environment Variables

Optional configuration via `.env` file:
```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CORS_ORIGINS=http://localhost:3000
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

## Running Tests

```bash
python manage.py test
```

## Database

SQLite is used by default. The database file `db.sqlite3` stores:
- Uploaded datasets (last 5 only)
- CSV file data
- Summary statistics
- User accounts

## Deployment

The project includes `Procfile` and production-ready settings for deployment to platforms like Render or Heroku.
