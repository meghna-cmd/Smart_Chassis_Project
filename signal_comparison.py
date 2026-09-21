
import pandas as pd
import numpy as np

file = "vehicle_vibration.xlsx.xlsx"

data = pd.read_excel(file, header=None)
data = data.iloc[5:, 2:]

data.columns = [
    "Crack1_30", "Crack1_50",
    "Crack2_30", "Crack2_50",
    "Crack3_30", "Crack3_50",
    "Crack4_30", "Crack4_50",
    "Crack5_30", "Crack5_50",
    "Crack6_30", "Crack6_50"
]

data = data.apply(pd.to_numeric, errors="coerce")

results = []

for column in data.columns:

    signal = data[column].dropna()

    absolute_signal = signal.abs()

    threshold = absolute_signal.quantile(0.98)

    anomaly_count = (absolute_signal > threshold).sum()

    anomaly_percentage = (
        anomaly_count / len(signal)
    ) * 100

    rms = np.sqrt(np.mean(signal ** 2))

    results.append({
        "Signal": column,
        "RMS": rms,
        "Standard Deviation": signal.std(),
        "Peak-to-Peak": signal.max() - signal.min(),
        "Anomaly Count": anomaly_count,
        "Anomaly Percentage": anomaly_percentage
    })

summary = pd.DataFrame(results)

print(summary.round(4))

summary.to_csv(
    "signal_comparison.csv",
    index=False
)

print("\nSignal Comparison Completed")