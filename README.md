📊 Chemical Equipment Parameter Visualizer
Hybrid Web + Desktop Application

📌 Project Overview:

The Chemical Equipment Parameter Visualizer is a hybrid application developed using Django, React, and PyQt5. It allows users to upload CSV files containing chemical equipment parameters and visualize the data through interactive charts and tables on both Web and Desktop platforms.

The system uses a common Django REST API backend that processes the data, performs analytics using Pandas, and serves the results to both frontends.

🚀 Key Features:

✅ Upload CSV files from Web and Desktop applications
✅ Parse and analyze data using Pandas
✅ Display equipment details in tabular format
✅ Generate interactive charts (Chart.js & Matplotlib)
✅ Summary statistics (count, averages, distributions)
✅ Store last 5 uploaded datasets (SQLite)
✅ RESTful API using Django REST Framework
✅ Basic Authentication (Optional Feature)
✅ PDF Report Generation (Optional Feature)

📁 Project Structure


<img width="832" height="577" alt="image" src="https://github.com/user-attachments/assets/ae14bd5c-dfae-40c1-9ed6-7dec1817fca7" />

⚙️ Installation & Setup
🔹 Prerequisites
Python 3.8+
Node.js
npm
Git

🔸 Backend Setup (Django)

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver


Backend runs on:

http://127.0.0.1:8000/

🔸 Web Frontend Setup (React)
cd web-frontend
npm install
npm start

Web app runs on:
http://localhost:3000/

🔸 Desktop App Setup (PyQt5)
cd desktop-app

pip install -r requirements.txt
python main.py

📡 API Endpoints
Endpoint	Method	Description
/api/upload/	POST	Upload CSV
/api/summary/	GET	Get statistics
/api/history/	GET	Last 5 uploads
/api/report/	GET	PDF Report
📊 Data Analytics

The backend performs:

Total equipment count

Average Flowrate

Average Pressure

Average Temperature

Equipment type distribution

Historical dataset tracking

Using Pandas for data processing.

📈 Visualization
Web (React + Chart.js)

Bar Charts
Pie Charts
Line Charts
Data Tables
Desktop (PyQt5 + Matplotlib)
Embedded Charts
Data Tables

Summary View:

Both frontends consume the same API for consistency.

📂 Sample Data

Sample CSV file provided:

sample_equipment_data.csv


Columns:

Equipment Name
Type
Flowrate
Pressure
Temperature

Used for testing and demonstration.

🔐 Authentication (Optional)

Basic user authentication implemented

Login required for uploading and reports

Django authentication system used

📄 PDF Report (Optional)

Generates downloadable PDF
Contains:
Summary statistics
Charts
Equipment table
Generated using backend API

🧪 Testing:

Manual testing for file upload

API tested using Postman

Cross-platform UI testing

📝 How to Use:

1️⃣ Start Django Backend

2️⃣ Run React Web App OR PyQt Desktop App

3️⃣ Upload CSV file

4️⃣ View data table and charts

5️⃣ Download report (optional)
