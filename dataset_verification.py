
import pandas as pd
import numpy as np

# -------------------------------
# LOAD DATASET
# -------------------------------

file = "vehicle_vibration.xlsx.xlsx"

data = pd.read_excel(file, header=None)

print("ORIGINAL DATASET SHAPE:", data.shape)

# -------------------------------
# DATA PREPROCESSING
# -------------------------------

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
# DATASET INFORMATION
# -------------------------------

print("\nDATASET VERIFICATION REPORT")
print("-" * 40)

print("Processed Dataset Shape:", data.shape)

print("\nColumn Names:")

for column in data.columns:
    print("-", column)

# -------------------------------
# MISSING VALUES
# -------------------------------

print("\nMISSING VALUES")

missing_values = data.isnull().sum()

print(missing_values)

# -------------------------------
# DUPLICATE ROWS
# -------------------------------

duplicate_rows = data.duplicated().sum()

print("\nDUPLICATE ROWS:", duplicate_rows)

# -------------------------------
# DATA TYPES
# -------------------------------

print("\nDATA TYPES")

print(data.dtypes)

# -------------------------------
# SIGNAL LENGTH
# -------------------------------

print("\nSIGNAL LENGTH")

for column in data.columns:

    signal = data[column].dropna()

    print(column, ":", len(signal), "samples")

# -------------------------------
# BASIC STATISTICS
# -------------------------------

print("\nBASIC STATISTICS")

statistics = data.describe().T

print(
    statistics[
        ["count", "mean", "std", "min", "max"]
    ].round(4)
)

# -------------------------------
# DATA QUALITY STATUS
# -------------------------------

print("\nDATA QUALITY STATUS")

if data.isnull().sum().sum() == 0:

    print("No missing values found.")

else:

    print("Missing values detected.")

if duplicate_rows == 0:

    print("No duplicate rows found.")

else:

    print("Duplicate rows detected.")

print("\nDataset Verification Completed")