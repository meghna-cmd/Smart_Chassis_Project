import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

train = pd.read_csv("train_features.csv")
test = pd.read_csv("test_features.csv")

scaler = StandardScaler()

train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(train_scaled)

train_prediction = model.predict(train_scaled)
test_prediction = model.predict(test_scaled)

train_anomalies = (train_prediction == -1).sum()
test_anomalies = (test_prediction == -1).sum()

train_percentage = train_anomalies / len(train_prediction) * 100
test_percentage = test_anomalies / len(test_prediction) * 100

print("TRAINING DATA EVALUATION")
print("Total Samples:", len(train_prediction))
print("Anomalies:", train_anomalies)
print("Anomaly Percentage:", round(train_percentage, 2), "%")

print("\nTESTING DATA EVALUATION")
print("Total Samples:", len(test_prediction))
print("Anomalies:", test_anomalies)
print("Anomaly Percentage:", round(test_percentage, 2), "%")

print("\nModel Evaluation Completed Successfully!")