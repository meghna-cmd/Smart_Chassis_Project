
# Smart Chassis Vibration Analysis System

## 1. Project Overview

The Smart Chassis Vibration Analysis System is a software-based prototype designed to analyze vehicle vibration signals and identify unusual vibration patterns.

The system uses statistical analysis, frequency-domain analysis, feature engineering, and machine learning-based anomaly detection.

The purpose of this project is to support early identification of potentially abnormal chassis vibration behavior.

## 2. Problem Statement

Vehicle chassis components experience vibrations due to road conditions, mechanical loads, and structural behavior.

Unusual vibration patterns may indicate the need for further inspection.

Manual monitoring can be difficult when large amounts of sensor data are involved.

This project analyzes vibration data computationally and highlights unusual patterns for further investigation.

## 3. Objectives

- Analyze vehicle vibration signals.
- Calculate important statistical features.
- Perform time-domain analysis.
- Perform frequency-domain analysis using FFT.
- Detect unusual vibration patterns.
- Compare different anomaly detection approaches.
- Display results through an interactive dashboard.
- Generate downloadable analysis reports.

## 4. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Scikit-learn
- OpenPyXL

## 5. System Methodology

### Step 1: Data Collection

A vehicle vibration dataset is loaded from an Excel file.

### Step 2: Data Preprocessing

- Unnecessary rows and columns are removed.
- Column names are assigned.
- Values are converted into numeric format.
- Missing values are handled by removing invalid entries during analysis.

### Step 3: Statistical Feature Extraction

The following features are calculated:

- Root Mean Square (RMS)
- Standard Deviation
- Peak-to-Peak Value
- Crest Factor

### Step 4: Frequency Analysis

Fast Fourier Transform (FFT) is used to analyze the frequency-domain characteristics of vibration signals.

The sampling rate is unavailable, so the frequency axis is represented using normalized frequency.

### Step 5: Anomaly Detection

The project uses multiple approaches:

1. Percentile-based anomaly detection
2. Isolation Forest
3. Feature-based anomaly detection

These methods identify unusual vibration patterns in the dataset.

### Step 6: Risk Scoring

A prototype risk scoring mechanism categorizes unusual vibration percentages into Low, Medium, and High levels.

These levels are intended for demonstration and analysis only.

### Step 7: Dashboard Development

An interactive Streamlit dashboard displays:

- Signal selection
- Statistical features
- Time-domain graphs
- Frequency-domain graphs
- Anomaly information
- Risk level
- Signal comparison
- Downloadable CSV reports

## 6. Project Outputs

The project generates the following output files:

- vibration_features.csv
- signal_comparison.csv
- advanced_data_quality_report.csv
- feature_based_anomaly_results.csv
- risk_scoring_results.csv
- final_model_comparison.csv

## 7. Limitations

- This is a software-based prototype.
- The dataset does not provide verified structural-damage labels.
- Anomalies do not confirm actual cracks or structural damage.
- The sampling rate is unavailable.
- Risk thresholds are prototype assumptions.
- The model has not been validated through physical vehicle testing.
- Real-world deployment requires calibrated sensors and validated datasets.

## 8. Future Scope

- Integrate real-time accelerometer sensors.
- Use labelled vibration datasets.
- Perform supervised machine learning.
- Add model evaluation metrics.
- Include real-time dashboard monitoring.
- Develop an alert system for abnormal vibration patterns.
- Validate results through laboratory and vehicle testing.

## 9. Conclusion

The Smart Chassis Vibration Analysis System demonstrates how vibration data can be processed using statistical analysis, signal processing, and machine learning techniques.

The prototype provides an interactive platform for exploring vibration behavior and identifying unusual patterns that may require further inspection.

The system should be considered a research and demonstration prototype rather than a certified structural-damage detection system.