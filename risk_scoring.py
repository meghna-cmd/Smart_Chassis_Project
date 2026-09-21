import pandas as pd
import numpy as np

# Dataset path
file = "vehicle_vibration.xlsx.xlsx"

# Read dataset
data = pd.read_excel(file, header=None)

# Remove unnecessary rows and columns
data = data.iloc[5:, 2:]

# Assign column names
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

results = []

for column in data.columns:

    signal = data[column].dropna().to_numpy()

    if len(signal) == 0:
        continue

    absolute_signal = np.abs(signal)

    # Statistical features
    rms = np.sqrt(np.mean(signal ** 2))

    standard_deviation = np.std(signal)

    peak_to_peak = np.max(signal) - np.min(signal)

    peak_value = np.max(absolute_signal)

    if rms != 0:
        crest_factor = peak_value / rms
    else:
        crest_factor = 0

    # Percentile-based anomaly detection
    threshold = np.percentile(absolute_signal, 98)

    anomaly_count = np.sum(absolute_signal > threshold)

    anomaly_percentage = (anomaly_count / len(signal)) * 100

    # Risk level
    if anomaly_percentage >= 7:
        risk_level = "High"
    elif anomaly_percentage >= 5:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    results.append({
        "Signal": column,
        "RMS": round(rms, 4),
        "Standard Deviation": round(standard_deviation, 4),
        "Peak-to-Peak": round(peak_to_peak, 4),
        "Crest Factor": round(crest_factor, 4),
        "Anomaly Count": int(anomaly_count),
        "Anomaly Percentage": round(anomaly_percentage, 2),
        "Risk Level": risk_level
    })

# Create result DataFrame
results_df = pd.DataFrame(results)

# Save results
results_df.to_csv("risk_scoring_results.csv", index=False)

# Display results
print("\nRisk Scoring Results:\n")
print(results_df.to_string(index=False))

print("\nRisk scoring completed.")
print("Results saved to risk_scoring_results.csv")

print("\nImportant:")
print("Risk levels represent unusual vibration patterns.")
print("They do not confirm actual structural damage.")