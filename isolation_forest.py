
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.ensemble import IsolationForest

from project_config import (
    CONTAMINATION,
    RANDOM_STATE,
    N_ESTIMATORS
)


# Output folder তৈরি
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)


# Step 1: Dataset খোঁজা
possible_files = [
    Path("outputs/clean_vibration_dataset.csv"),
    Path("clean_vibration_dataset.csv"),
    Path("data/clean_vibration_dataset.csv"),
    Path("outputs/feature_engineering_results.csv")
]

input_file = None

for file in possible_files:
    if file.exists():
        input_file = file
        break


if input_file is None:
    print("Dataset file পাওয়া যায়নি!")
    print("Available CSV files:")

    for file in Path(".").rglob("*.csv"):
        print(file)

    raise FileNotFoundError(
        "Required dataset file পাওয়া যায়নি।"
    )


# Step 2: Dataset Load
print("Loading file:", input_file)

data = pd.read_csv(input_file)


# Step 3: Numeric Columns নির্বাচন
numeric_data = data.select_dtypes(
    include=np.number
)

numeric_data = numeric_data.replace(
    [np.inf, -np.inf],
    np.nan
)

numeric_data = numeric_data.dropna()


if numeric_data.empty:
    raise ValueError(
        "Dataset-এ কোনো valid numeric data নেই।"
    )


# Step 4: Isolation Forest Model
model = IsolationForest(
    contamination=CONTAMINATION,
    random_state=RANDOM_STATE,
    n_estimators=N_ESTIMATORS
)


# Step 5: Model Train
model.fit(numeric_data)


# Step 6: Anomaly Prediction
predictions = model.predict(numeric_data)

anomaly_scores = model.decision_function(
    numeric_data
)


# Step 7: Results তৈরি
result_df = numeric_data.copy()

result_df["Anomaly_Label"] = predictions

result_df["Anomaly_Score"] = anomaly_scores

result_df["Anomaly_Status"] = np.where(
    predictions == -1,
    "Anomaly",
    "Normal"
)


# Step 8: Results Save
output_file = (
    output_folder / "isolation_forest_results.csv"
)

result_df.to_csv(
    output_file,
    index=False
)


# Step 9: Summary
total_records = len(result_df)

anomaly_count = np.sum(
    predictions == -1
)

anomaly_percentage = (
    anomaly_count / total_records
) * 100


print("\nSMART CHASSIS ISOLATION FOREST")
print("----------------------------------------")

print("Input File:", input_file)

print("Contamination:", CONTAMINATION)

print("Random State:", RANDOM_STATE)

print("Estimators:", N_ESTIMATORS)

print("Total Records:", total_records)

print("Anomaly Count:", anomaly_count)

print(
    "Anomaly Percentage:",
    round(anomaly_percentage, 2),
    "%"
)

print("\nResults saved successfully!")

print("Output File:", output_file)