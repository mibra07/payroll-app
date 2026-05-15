# ----------------------------------
# BACKEND
# ----------------------------------

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

# ----------------------------------
# FRONTEND
# ----------------------------------

# Payroll Frontend Dashboard

A React frontend dashboard for the Payroll API.

# Features

CSV upload
Payroll summary table
Filtering
Sorting
Pagination
CSV export
API integration

# Tech Stack

⚛️ React
📡 Axios
🎨 CSS
⚡ Vite

# Frontend Structure

frontend/
│
├── src/
│   ├── App.jsx
│   ├── api.js
│   ├── styles.css
│   │
│   └── components/
│       ├── UploadForm.jsx
│       └── SummaryTable.jsx
│
├── package.json
└── README.md

# Setup

STEP 1 → Install Dependencies
npm install
STEP 2 → Install Axios
npm install axios
STEP 3 → Start Development Server
npm run dev


Frontend URL:
http://localhost:5173

# API Configuration

Inside:src/api.js

Set backend URL:
baseURL: "http://localhost:8000"

# Frontend Components

UploadForm.jsx
Handles:
Config CSV upload
Clock record CSV upload
Error handling
Loading states

SummaryTable.jsx
Handles:
Payroll summary display
Filters
Sorting
Pagination
CSV download

# Frontend Flow

User Action
    ↓
React Component
    ↓
Axios API Request
    ↓
FastAPI Backend
    ↓
Database Response
    ↓
React UI Update


# API Functions

Upload File:
uploadFile(url, file)
Used for:
/configs
/clock-records

Get Summary:
getSummary(params)
Used for:
filtering
sorting
pagination

Generate CSV URL:
getCSVUrl(params)
Used for:
CSV export download

# Debugging

Browser Console
console.log("API response:", response.data);

# Network Tab

Open: Chrome DevTools → Network
Check:
request URL
query params
API response
CSV download

# CSS Features

Responsive layout
Dashboard cards
Styled table
Hover effects
Pagination controls
Loading/error states

# Concepts Covered

React Hooks
useState
useEffect
Axios
Async/Await
File Upload
Controlled Components
API Integration
Pagination UI
Conditional Rendering




# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is enabled on this template. See [this documentation](https://react.dev/learn/react-compiler) for more information.

Note: This will impact Vite dev & build performances.

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.