
import pandas as pd

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

print("Dataset Shape:", data.shape)

print("\nMissing Values:")
print(data.isnull().sum())

print("\nDuplicate Rows:", data.duplicated().sum())

print("\nData Types:")
print(data.dtypes)

print("\nData Quality Check Completed")