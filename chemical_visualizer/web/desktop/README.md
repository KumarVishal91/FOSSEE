# Chemical Equipment Parameter Visualizer - Desktop App

PyQt5 desktop application for visualizing chemical equipment data.

## Features
- CSV file upload
- Interactive charts (Matplotlib)
- Data table view
- Summary statistics with min/max values
- PDF report download
- Authentication (Basic Auth)
- History of last 5 datasets

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Prerequisites

- Python 3.8+
- Backend API running at `http://127.0.0.1:8000/api`

## Configuration

The desktop app connects to the backend API at:
```python
API_URL = "http://127.0.0.1:8000/api"
```

To change this, edit the `API_URL` constant in [app.py](app.py#L23).

## Usage

1. Enter your credentials (default: admin/admin123)
2. Click "Upload CSV" to select and upload a file
3. View charts, tables, and statistics
4. Download PDF reports
5. Access previous uploads from the history list

## Technologies
- PyQt5
- Matplotlib
- Requests
- Python 3.13
