# 🚌 TRANSPORT-PANIMALAR
AI Powered College Bus Monitoring System

## 📌 Project Overview

TRANSPORT-PANIMALAR is an AI-based bus monitoring system developed to track college bus arrivals automatically using vehicle number plate recognition.

The system captures a bus number plate using a camera, extracts the plate number using OCR (EasyOCR), verifies it with a bus database, and records the arrival in a dashboard similar to an airport arrival board.

This helps transport administrators monitor bus arrivals efficiently.

---

## 🚀 Features

- 📷 Camera-based bus number plate scanning
- 🤖 AI OCR number plate detection using EasyOCR
- 📊 Live dashboard showing bus arrivals
- 🛬 Airport-style arrival board
- 🗂 Bus database management (Add / Delete buses)
- 🔐 Admin login for capture system
- 📄 PDF and CSV report generation
- 📱 Mobile-compatible dashboard
- 🔄 Auto-refresh live arrival monitoring

---

## 🧠 Technologies Used

| Technology | Purpose |
|------------|--------|
| Python | Core programming language |
| Streamlit | Web dashboard framework |
| EasyOCR | AI text recognition |
| OpenCV | Image processing |
| SQLite | Local database |
| Plotly | Data visualization |
| ReportLab | PDF report generation |

---

## 🏗 System Workflow

1. Capture bus image using camera
2. Process image with OpenCV
3. Detect text using EasyOCR
4. Extract number plate pattern
5. Verify bus in database
6. Record arrival with timestamp
7. Display on live dashboard

---

## 📊 Dashboard Modules

### Dashboard
Displays:
- Total buses
- Arrived buses
- Pending buses
- Arrival board

### Capture Bus
- Scan number plate
- Detect bus automatically
- Record arrival

### Manage Buses
- Add buses
- Delete buses
- View database

### Reports
- Download CSV reports
- Generate PDF reports

---
project-folder
│
├── app.py
├── logo.png
├── image.png
├── bus_system.db
├── reports/
├── requirements.txt
└── README.md


---

## 🌐 Deployment

The application can be deployed easily using:

- Streamlit Community Cloud
- Render
- Railway
- HuggingFace Spaces

---

## 🎓 Use Case

This project is designed for:

- College transport monitoring
- Smart campus systems
- AI-based vehicle tracking
- Automated entry systems

---

## 👨‍💻 Developer

Adhityan  
Panimalar Engineering College

AI Transport Monitoring Prototype
