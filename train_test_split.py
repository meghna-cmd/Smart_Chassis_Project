import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_FILE = "clean_vibration_dataset.csv"

data = pd.read_csv(INPUT_FILE)

print("Dataset Shape:", data.shape)

# Select complete columns only
data = data.dropna(axis=1)

print("Shape After Removing Missing Columns:", data.shape)

# Split columns into train and test
train_data, test_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

train_data.to_csv("train_dataset.csv", index=False)
test_data.to_csv("test_dataset.csv", index=False)

print("\nTraining Dataset Shape:", train_data.shape)
print("Testing Dataset Shape:", test_data.shape)

print("\nTrain-Test Split Completed Successfully!")