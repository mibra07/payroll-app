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