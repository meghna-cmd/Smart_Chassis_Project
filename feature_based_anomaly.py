
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
# SETTINGS
# -------------------------------

window_size = 100

results = []

# -------------------------------
# FEATURE EXTRACTION
# -------------------------------

for column in data.columns:

    signal = data[column].dropna().to_numpy()

    windows = []

    for start in range(
        0,
        len(signal) - window_size + 1,
        window_size
    ):

        window = signal[
            start:start + window_size
        ]

        rms = np.sqrt(
            np.mean(window ** 2)
        )

        standard_deviation = np.std(window)

        peak_to_peak = (
            np.max(window) - np.min(window)
        )

        windows.append([
            rms,
            standard_deviation,
            peak_to_peak
        ])

    features = np.array(windows)

    if len(features) < 10:

        print(column, "Skipped: insufficient windows")

        continue

    # -------------------------------
    # ISOLATION FOREST
    # -------------------------------

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(features)

    anomaly_count = np.sum(
        predictions == -1
    )

    anomaly_percentage = (
        anomaly_count / len(predictions)
    ) * 100

    results.append({

        "Signal": column,

        "Total Windows": len(features),

        "Anomaly Windows": int(
            anomaly_count
        ),

        "Anomaly Percentage": round(
            anomaly_percentage, 2
        )

    })

    print(
        column,
        "| Total Windows:",
        len(features),
        "| Anomaly Windows:",
        anomaly_count,
        "| Percentage:",
        round(anomaly_percentage, 2),
        "%"
    )

# -------------------------------
# SAVE RESULTS
# -------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "feature_based_anomaly_results.csv",
    index=False
)

print("\nFeature-Based Anomaly Detection Completed.")

print(
    "Results saved to feature_based_anomaly_results.csv"
)

print(
    "\nNote: Anomalies indicate unusual feature patterns."
)

print(
    "They do not confirm actual structural damage."
)