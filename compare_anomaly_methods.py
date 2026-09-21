
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest

# -------------------------------
# LOAD DATASET
# -------------------------------

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

# -------------------------------
# COMPARE METHODS
# -------------------------------

results = []

for column in data.columns:

    signal = data[column].dropna()

    values = signal.to_numpy().reshape(-1, 1)

    # Method 1: Percentile Detection
    absolute_signal = signal.abs()

    threshold = absolute_signal.quantile(0.98)

    percentile_anomalies = (
        absolute_signal > threshold
    )

    percentile_count = percentile_anomalies.sum()

    percentile_percentage = (
        percentile_count / len(signal)
    ) * 100

    # Method 2: Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    predictions = model.fit_predict(values)

    isolation_count = np.sum(
        predictions == -1
    )

    isolation_percentage = (
        isolation_count / len(signal)
    ) * 100

    # Store results
    results.append({

        "Signal": column,

        "Total Samples": len(signal),

        "Percentile Anomalies": int(
            percentile_count
        ),

        "Percentile Percentage": round(
            percentile_percentage, 2
        ),

        "Isolation Forest Anomalies": int(
            isolation_count
        ),

        "Isolation Forest Percentage": round(
            isolation_percentage, 2
        )

    })

# -------------------------------
# CREATE COMPARISON TABLE
# -------------------------------

comparison_df = pd.DataFrame(results)

print("ANOMALY DETECTION COMPARISON")
print("-" * 80)

print(
    comparison_df.to_string(index=False)
)

# -------------------------------
# SAVE RESULTS
# -------------------------------

comparison_df.to_csv(
    "anomaly_method_comparison.csv",
    index=False
)

print("\nComparison report saved successfully.")

print(
    "\nNote: Anomalies do not confirm "
    "actual structural damage."
)

print(
    "Comparison Analysis Completed."
)