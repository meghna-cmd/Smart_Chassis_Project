
import pandas as pd

file = "vehicle_vibration.xlsx.xlsx"

# Read Excel file
data = pd.read_excel(file, header=None)

# Remove unnecessary rows and columns
data = data.iloc[5:, 2:]

# Set column names
data.columns = [
    "Crack1_30", "Crack1_50",
    "Crack2_30", "Crack2_50",
    "Crack3_30", "Crack3_50",
    "Crack4_30", "Crack4_50",
    "Crack5_30", "Crack5_50",
    "Crack6_30", "Crack6_50"
]

# Convert values into numeric format
data = data.apply(pd.to_numeric, errors="coerce")

# Select vibration signal
signal = data["Crack1_30"].dropna()

# Convert values to absolute values
absolute_signal = signal.abs()

# Calculate threshold using 98th percentile
threshold = absolute_signal.quantile(0.98)

# Detect abnormal vibration
anomalies = absolute_signal > threshold

# Calculate anomaly count and percentage
anomaly_count = anomalies.sum()

anomaly_percentage = (anomaly_count / len(signal)) * 100

# Display results
print("Selected Signal: Crack1_30")

print("Total Data Points:", len(signal))

print("Abnormal Vibration Count:", anomaly_count)

print(
    "Abnormal Vibration Percentage:",
    round(anomaly_percentage, 2),
    "%"
)

print("Detection Threshold:", round(threshold, 4))

# Warning system
if anomaly_percentage > 5:
    print("WARNING: High Abnormal Vibration Rate!")
    print("Potential Structural Issue - Prototype Result")
else:
    print("Status: Normal Vibration")
    print("No High Abnormal Vibration Rate Detected")