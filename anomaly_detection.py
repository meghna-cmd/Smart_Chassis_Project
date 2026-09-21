
import pandas as pd
import numpy as np

from project_config import (
    PERCENTILE_THRESHOLD,
    DATASET_FILE
)


# Step 1: Load Dataset
data = pd.read_excel(DATASET_FILE, header=None)


# Step 2: Clean Dataset
data = data.iloc[5:, 2:]

data.columns = [
    "Crack1_30",
    "Crack1_50",
    "Crack2_30",
    "Crack2_50",
    "Crack3_30",
    "Crack3_50",
    "Crack4_30",
    "Crack4_50",
    "Crack5_30",
    "Crack5_50",
    "Crack6_30",
    "Crack6_50"
]

data = data.apply(pd.to_numeric, errors="coerce")


# Step 3: Anomaly Detection
results = []

for column in data.columns:

    signal = data[column].dropna().to_numpy()

    if len(signal) == 0:
        continue

    absolute_signal = np.abs(signal)

    # Threshold from configuration file
    threshold = np.percentile(
        absolute_signal,
        PERCENTILE_THRESHOLD
    )

    anomaly_values = absolute_signal > threshold

    anomaly_count = np.sum(anomaly_values)

    total_values = len(signal)

    anomaly_percentage = (
        anomaly_count / total_values
    ) * 100

    # Warning Level
    if anomaly_percentage > 7:
        warning = "HIGH"

    elif anomaly_percentage >= 5:
        warning = "MEDIUM"

    else:
        warning = "LOW"

    results.append({
        "Signal": column,
        "Total Values": total_values,
        "Threshold": threshold,
        "Anomaly Count": anomaly_count,
        "Anomaly Percentage": round(
            anomaly_percentage, 2
        ),
        "Warning Level": warning
    })


# Step 4: Create Result DataFrame
result_df = pd.DataFrame(results)


# Step 5: Display Results
print("\nSMART CHASSIS ANOMALY DETECTION")
print("----------------------------------------")

print(
    "Percentile Threshold:",
    PERCENTILE_THRESHOLD
)

print(result_df.to_string(index=False))


# Step 6: Save Results
result_df.to_csv(
    "outputs/anomaly_detection_results.csv",
    index=False
)

print("\nResults saved successfully.")