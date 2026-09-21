import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

TRAIN_FILE = "train_features.csv"
TEST_FILE = "test_features.csv"

train_data = pd.read_csv(TRAIN_FILE)
test_data = pd.read_csv(TEST_FILE)

# Feature scaling
scaler = StandardScaler()

train_scaled = scaler.fit_transform(train_data)
test_scaled = scaler.transform(test_data)

# Create ML model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# Train model
model.fit(train_scaled)

# Predict anomalies
predictions = model.predict(test_scaled)

test_data["Prediction"] = predictions

# -1 means anomaly, 1 means normal
anomaly_count = (predictions == -1).sum()
total_samples = len(predictions)

anomaly_percentage = (anomaly_count / total_samples) * 100

print("Total Test Samples:", total_samples)
print("Anomalies Detected:", anomaly_count)
print("Anomaly Percentage:", round(anomaly_percentage, 2), "%")

if anomaly_percentage > 5:
    print("Warning: Unusual vibration pattern detected!")
else:
    print("Status: Normal vibration pattern.")

test_data.to_csv("ml_anomaly_results.csv", index=False)

print("\nML Isolation Forest Completed Successfully!")