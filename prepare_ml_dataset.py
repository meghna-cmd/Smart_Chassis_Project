
import pandas as pd
from pathlib import Path

# -----------------------------------------
# Configuration
# -----------------------------------------

INPUT_FILE = "vehicle_vibration.xlsx.xlsx"
OUTPUT_FILE = "clean_vibration_dataset.csv"

# -----------------------------------------
# Check dataset
# -----------------------------------------

if not Path(INPUT_FILE).exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}"
    )

# -----------------------------------------
# Load dataset
# -----------------------------------------

data = pd.read_excel(
    INPUT_FILE,
    header=None
)

# Remove unnecessary rows and columns
data = data.iloc[5:, 2:].copy()

# Assign column names
data.columns = [
    "Crack1_30", "Crack1_50",
    "Crack2_30", "Crack2_50",
    "Crack3_30", "Crack3_50",
    "Crack4_30", "Crack4_50",
    "Crack5_30", "Crack5_50",
    "Crack6_30", "Crack6_50"
]

# Convert to numeric
data = data.apply(
    pd.to_numeric,
    errors="coerce"
)

# -----------------------------------------
# Data quality summary
# -----------------------------------------

print("\nOriginal Dataset Shape:")
print(data.shape)

print("\nMissing Values Before Cleaning:")
print(data.isna().sum())

# -----------------------------------------
# Remove completely empty columns
# -----------------------------------------

data = data.dropna(
    axis=1,
    how="all"
)

# -----------------------------------------
# Save clean dataset
# -----------------------------------------

data.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nClean Dataset Shape:")
print(data.shape)

print("\nMissing Values After Cleaning:")
print(data.isna().sum())

print("\nClean dataset saved successfully.")
print(f"Output File: {OUTPUT_FILE}")

print(
    "\nNote: Missing values are retained as NaN "
    "for transparent data-quality handling."
)