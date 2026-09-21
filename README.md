
# 🚗 Smart Chassis Vibration Analysis System

<p align="center">
  <strong>Intelligent Vehicle Vibration Monitoring & Anomaly Detection</strong>
</p>

<p align="center">
  A Python-based academic prototype for analyzing vehicle chassis vibration signals, extracting features, and identifying abnormal vibration patterns.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit">
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-green?logo=fastapi">
  <img src="https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite">
  <img src="https://img.shields.io/badge/Project-Academic%20Prototype-purple">
</p>

---

## 🌟 Project Overview

The **Smart Chassis Vibration Analysis System** is a software-based academic prototype designed to analyze vehicle chassis vibration signals and identify abnormal vibration patterns.

The system combines signal processing, statistical feature extraction, machine learning, simulated sensor data, interactive visualization, FastAPI, and SQLite database integration.

The project focuses on vibration monitoring and anomaly detection to support further research into vehicle chassis health monitoring.

---

## 🎯 Objectives

- Analyze vehicle chassis vibration signals.
- Extract important vibration features.
- Detect abnormal vibration patterns.
- Perform frequency-domain analysis.
- Display warning and risk indications.
- Store analysis results in a database.
- Provide API-based vibration analysis.
- Support visualization through an interactive dashboard.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming and analysis |
| Pandas | Data processing |
| NumPy | Numerical computation |
| Matplotlib | Data visualization |
| Plotly | Interactive visualization |
| Scikit-learn | Machine learning and anomaly detection |
| Streamlit | Interactive dashboard |
| FastAPI | REST API development |
| SQLite | Database storage |
| Uvicorn | API server |
| OpenPyXL | Excel file processing |

---

## ✨ Key Features

### 📊 Vibration Signal Analysis
- Signal preprocessing and analysis.
- Statistical feature extraction.
- Vibration pattern examination.

### 📉 Frequency-Domain Analysis
- Frequency-related feature extraction.
- Identification of abnormal frequency patterns.
- Support for vibration signal interpretation.

### 🔍 Anomaly Detection
- Machine learning-based anomaly detection.
- Feature-based analysis.
- Risk scoring and warning indications.

### 🖥️ Interactive Dashboard
- Streamlit-based visualization.
- Graphical representation of analysis results.
- Interactive monitoring interface.

### 📡 Sensor Simulation
- Simulated real-time vibration readings.
- Support for testing analysis workflows without physical sensors.

### 🔗 API & Database
- FastAPI-based REST API.
- SQLite database integration.
- Analysis result storage and retrieval.

---

## 🔄 Project Workflow

```text
Dataset / Simulated Sensor
          ↓
Data Preprocessing
          ↓
Feature Extraction
          ↓
Frequency Analysis
          ↓
Anomaly Detection
          ↓
Risk & Warning Analysis
          ↓
Dashboard / API Output
          ↓
Database Storage
```

---

## 📂 Project Structure

```text
Smart_Chassis_Project/
│
├── app.py
├── api.py
├── requirements.txt
├── README.md
│
├── data/
├── outputs/
│
├── anomaly_detection.py
├── feature_engineering.py
├── frequency_analysis.py
├── isolation_forest.py
├── risk_scoring.py
│
├── realtime_sensor.py
├── logging_config.py
├── error_handler.py
│
└── test_project_files.py
```

> The structure above highlights the main project components. The complete repository may contain additional analysis, validation, and testing files.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Smart_Chassis_Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

### 4. Run the FastAPI Server

```bash
uvicorn api:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Run Tests

```bash
python -m unittest discover -v
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health status |
| POST | `/analyze` | Analyze vibration readings |
| GET | `/analyses` | View saved analyses |

> Verify endpoint availability and behavior against the current API implementation.

---

## 📈 Analysis & Machine Learning

The project includes components for:

- Statistical vibration feature extraction.
- Frequency analysis.
- Isolation Forest-based anomaly detection.
- Feature-based anomaly analysis.
- Risk scoring.
- Model comparison and evaluation.

The anomaly detection system identifies unusual patterns in the analyzed signals. These results do not directly confirm physical cracks or structural damage.

---

## ⚠️ Limitations

This project is an **academic software prototype**.

- Sensor readings are simulated rather than collected from a physical accelerometer.
- Verified structural-damage labels are unavailable.
- Anomaly detection does not directly confirm cracks or structural damage.
- Real vehicle testing has not been performed.
- Frequency results may use normalized frequency where actual sampling-rate information is unavailable.
- Further validation is required before real-world safety deployment.

---

## 🔮 Future Scope

- Physical accelerometer integration.
- Microcontroller connectivity.
- Verified structural-damage datasets.
- Real vehicle testing.
- Improved machine learning model validation.
- Real-time monitoring enhancements.
- Cloud deployment and monitoring.
- Advanced predictive maintenance research.

---

## 🧪 Project Testing

The project includes testing and validation components for checking project files and analysis workflows.

Testing should be performed using the available test scripts and documented with their actual results.

---

## 👩‍💻 Author

**Meghna Mukherjee**

B.Tech Engineering Student

---

## 📌 Project Status

**Academic Prototype — Development and Testing**

The project includes vibration analysis, anomaly detection, dashboard visualization, sensor simulation, API integration, database storage, logging, and testing components.

Further validation and real-world sensor testing are required for future development.