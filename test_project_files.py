
from pathlib import Path
import pandas as pd

print("SMART CHASSIS PROJECT VALIDATION")
print("-" * 40)

required_files = [
    "vehicle_vibration.xlsx.xlsx",
    "clean_vibration_dataset.csv",
    "train_dataset.csv",
    "test_dataset.csv",
    "train_features.csv",
    "test_features.csv",
    "frequency_features.csv",
    "ml_anomaly_results.csv",
    "final_model_comparison.csv"
]

all_files_exist = True

for file in required_files:

    file_path = Path(file)

    if file_path.exists():
        print(f"[PASS] {file}")
    else:
        print(f"[FAIL] {file}")
        all_files_exist = False

print("\nDATA VALIDATION")
print("-" * 40)

try:

    train = pd.read_csv("train_features.csv")
    test = pd.read_csv("test_features.csv")

    expected_columns = [
        "RMS",
        "Standard_Deviation",
        "Peak_to_Peak"
    ]

    if list(train.columns) == expected_columns:
        print("[PASS] Training feature columns")
    else:
        print("[FAIL] Training feature columns")

    if list(test.columns) == expected_columns:
        print("[PASS] Testing feature columns")
    else:
        print("[FAIL] Testing feature columns")

    if train.isna().sum().sum() == 0:
        print("[PASS] Training data has no missing values")
    else:
        print("[FAIL] Training data contains missing values")

    if test.isna().sum().sum() == 0:
        print("[PASS] Testing data has no missing values")
    else:
        print("[FAIL] Testing data contains missing values")

except Exception as error:

    print("[FAIL] Data validation error:", error)
    all_files_exist = False

print("\nFINAL VALIDATION RESULT")
print("-" * 40)

if all_files_exist:
    print("Project validation completed.")
else:
    print("Some files or checks require attention.")