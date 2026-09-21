
import pandas as pd
import numpy as np

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

print("RMS VALIDATION REPORT")
print("-" * 30)

for column in data.columns:

    signal = data[column].dropna()

    rms = np.sqrt(np.mean(signal ** 2))

    print(column, "RMS:", round(rms, 4))

print("-" * 30)
print("Validation Completed")