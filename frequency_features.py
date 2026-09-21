import pandas as pd
import numpy as np

INPUT_FILE = "clean_vibration_dataset.csv"
OUTPUT_FILE = "frequency_features.csv"

data = pd.read_csv(INPUT_FILE)

results = []

for column in data.columns:
    signal = data[column].dropna().values

    # Remove DC component
    signal = signal - np.mean(signal)

    # Real FFT
    fft_values = np.fft.rfft(signal)
    magnitude = np.abs(fft_values)

    # Ignore zero-frequency component
    if len(magnitude) > 1:
        dominant_index = np.argmax(magnitude[1:]) + 1
    else:
        dominant_index = 0

    dominant_magnitude = magnitude[dominant_index]

    results.append({
        "Signal": column,
        "Dominant_Frequency_Index": dominant_index,
        "Dominant_Magnitude": round(
            dominant_magnitude, 4
        )
    })

frequency_data = pd.DataFrame(results)

frequency_data.to_csv(OUTPUT_FILE, index=False)

print(frequency_data)

print("\nImproved Frequency Analysis Completed Successfully!")