import pandas as pd
import numpy as np
import plotly.express as px

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

signal = data["Crack1_30"].dropna().values

fft_values = np.fft.fft(signal)
frequency = np.fft.fftfreq(len(signal))

magnitude = np.abs(fft_values)

result = pd.DataFrame({
    "Frequency": frequency,
    "Magnitude": magnitude
})

result = result[result["Frequency"] >= 0]

fig = px.line(
    result,
    x="Frequency",
    y="Magnitude",
    title="Frequency Analysis - Crack1 at 30 km/h"
)

fig.show()