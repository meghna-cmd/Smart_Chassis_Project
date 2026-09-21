
"""Model Validation for Smart Chassis Project"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest


# Project folder
PROJECT_ROOT = Path(__file__).resolve().parent

# Dataset is directly inside project folder
DATA_FILE = PROJECT_ROOT / "clean_vibration_dataset.csv"

# Output folder
OUTPUT_FOLDER = PROJECT_ROOT / "outputs"
OUTPUT_FOLDER.mkdir(exist_ok=True)


def run_validation():

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:
        raise ValueError(
            "No numeric vibration columns found."
        )

    results = []

    for signal in numeric_columns:

        values = df[signal].dropna().values.reshape(-1, 1)

        train_data, test_data = train_test_split(
            values,
            test_size=0.20,
            random_state=42
        )

        model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

        model.fit(train_data)

        predictions = model.predict(test_data)

        anomaly_count = int(
            (predictions == -1).sum()
        )

        anomaly_percentage = (
            anomaly_count / len(test_data)
        ) * 100

        results.append({
            "Signal": signal,
            "Test Samples": len(test_data),
            "Predicted Anomalies": anomaly_count,
            "Predicted Anomaly Percentage": round(
                anomaly_percentage, 2
            ),
            "Validation Type": (
                "Unsupervised holdout; "
                "no verified damage labels"
            )
        })

    result_df = pd.DataFrame(results)

    output_file = (
        OUTPUT_FOLDER / "model_validation_report.csv"
    )

    result_df.to_csv(
        output_file,
        index=False
    )

    print("\nMODEL VALIDATION RESULTS")
    print("-" * 40)
    print(result_df.to_string(index=False))

    print("\nModel validation completed successfully!")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    run_validation()