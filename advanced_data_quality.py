
import pandas as pd

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
# DATA QUALITY REPORT
# -------------------------------

report = []

for column in data.columns:

    signal = data[column]

    total_values = len(signal)

    valid_values = signal.notna().sum()

    missing_values = signal.isna().sum()

    missing_percentage = (
        missing_values / total_values
    ) * 100

    report.append({

        "Signal": column,

        "Total Values": total_values,

        "Valid Values": valid_values,

        "Missing Values": missing_values,

        "Missing Percentage": round(
            missing_percentage, 2
        )

    })

report_df = pd.DataFrame(report)

print("ADVANCED DATA QUALITY REPORT")
print("-" * 45)

print(report_df.to_string(index=False))

# -------------------------------
# SAVE REPORT
# -------------------------------

report_df.to_csv(
    "advanced_data_quality_report.csv",
    index=False
)

print("\nReport saved successfully.")

print(
    "\nMissing values are retained because "
    "signals may have different lengths."
)

print("Advanced Data Quality Check Completed.")