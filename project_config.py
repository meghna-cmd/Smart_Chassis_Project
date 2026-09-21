
# SMART CHASSIS PROJECT CONFIGURATION

# Anomaly Detection Settings
PERCENTILE_THRESHOLD = 98

# Feature Engineering Settings
WINDOW_SIZE = 100

# Machine Learning Settings
CONTAMINATION = 0.05
RANDOM_STATE = 42
N_ESTIMATORS = 100

# Warning System Settings
HIGH_RISK_THRESHOLD = 7
MEDIUM_RISK_THRESHOLD = 5

# Dataset Settings
DATASET_FILE = "vehicle_vibration.xlsx.xlsx"

# Output Files
FEATURE_FILE = "frequency_features.csv"
ML_RESULT_FILE = "ml_anomaly_results.csv"
COMPARISON_FILE = "final_model_comparison.csv"