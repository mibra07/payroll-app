# Payroll Backend API

A FastAPI-based payroll processing backend that:

Uploads CSV files
Stores payroll data in SQLite
Calculates late hours & overtime
Generates payroll summaries
Exports CSV reports

# Tech Stack

⚡ FastAPI
🗄 SQLite
🧠 SQLAlchemy
📄 CSV Processing
🔍 Pydantic Validation
🚀 Uvicorn

# Backend Structure

backend/
│
├── main.py
├── db.py
├── models.py
├── schemas.py
├── payroll.db
├── requirements.txt
├── services├── aggregation.py 
│           ├── csv_parser.py
└── README.md

# Setup

STEP 1 → Create Virtual Environment
python3 -m venv backend

STEP 2 → Activate Environment
Mac/Linux: source venv/bin/activate
Windows: venv\Scripts\activate

STEP 3 → Install Dependencies
pip install fastapi uvicorn sqlalchemy python-multipart

STEP 4 → Run Server
uvicorn main:app --reload

# API URL

http://127.0.0.1:8000

# Swagger Docs

http://127.0.0.1:8000/docs

# Database

SQLite database: payroll.db

# CSV Formats

configs.csv
Example:
employee_type,shift_start,shift_end,overtime_rate,late_cut_rate
full-time,09:00,18:00,10,5
part-time,10:00,16:00,8,4
contractor,11:00,17:00,12,6

clock-records.csv
Example:
employee_id,employee_type,clock_in,clock_out
101,full-time,09:15,18:30
102,part-time,10:05,16:20
103,contractor,11:10,17:40

# API Endpoints

Upload Configurations
POST /configs

Upload Clock Records
POST /clock-records

Get Payroll Summary
GET /summary

Query Parameters

| Parameter     | Example    |
| ------------- | ---------- |
| limit         | 50         |
| offset        | 0          |
| employee_type | full-time  |
| sort          | late_hours |
| order         | asc        |

Example: /summary?limit=50&offset=0&sort=late_hours&order=desc

Download CSV Report
GET /summary.csv
Example: /summary.csv?employee_type=full-time&sort=late_hours&order=asc

# Payroll Calculation Logic

Late Hours
clock_in > shift_start
Formula SQL: (clock_in - shift_start) / 3600

Overtime Hours
clock_out > shift_end
Formula SQL: (clock_out - shift_end) / 3600

Total Late Cut
late_hours × late_cut_rate

Total Overtime Pay
overtime_hours × overtime_rate

# Duplicate Prevention

Unique constraint: python
UniqueConstraint(
    "employee_id",
    "clock_in",
    "clock_out"
)

# Debugging

Backend Logs: python
print("STEP 1")
print("STEP 2")

# Concepts Covered

FastAPI Routing
SQLAlchemy ORM
SQLite
CSV Upload
StreamingResponse
Pagination
Filtering
Sorting
Aggregate SQL Queries
Dependency Injection
Error Handling