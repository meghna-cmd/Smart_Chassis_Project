import pandas as pd

file = "vehicle_vibration.xlsx.xlsx"

data = pd.read_excel(file, header=None)

# Remove first 5 heading rows
data = data.iloc[5:, 2:]

# Give proper column names
data.columns = [
    "Crack1_30",
    "Crack1_50",
    "Crack2_30",
    "Crack2_50",
    "Crack3_30",
    "Crack3_50",
    "Crack4_30",
    "Crack4_50",
    "Crack5_30",
    "Crack5_50",
    "Crack6_30",
    "Crack6_50"
]

# Convert values into numbers
data = data.apply(pd.to_numeric, errors="coerce")

print(data.head())
print(data.shape)
print(data.info())