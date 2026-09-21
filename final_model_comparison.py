import pandas as pd

# File paths
risk_file = "risk_scoring_results.csv"
feature_file = "feature_based_anomaly_results.csv"

# Read risk scoring results
risk_data = pd.read_csv(risk_file)

# Read feature-based anomaly results
feature_data = pd.read_csv(feature_file)

# Display column names for checking
print("Risk Scoring Columns:")
print(risk_data.columns.tolist())

print("\nFeature-Based Anomaly Columns:")
print(feature_data.columns.tolist())

# Select useful columns from risk scoring
risk_summary = risk_data[
    [
        "Signal",
        "RMS",
        "Standard Deviation",
        "Peak-to-Peak",
        "Crest Factor",
        "Anomaly Percentage",
        "Risk Level"
    ]
].copy()

# Rename anomaly percentage column
risk_summary = risk_summary.rename(
    columns={
        "Anomaly Percentage": "Percentile Anomaly Percentage"
    }
)

# Detect feature-based anomaly percentage column
possible_columns = [
    "Anomaly Percentage",
    "Feature Anomaly Percentage",
    "Anomaly_Percentage"
]

feature_percentage_column = None

for column in possible_columns:
    if column in feature_data.columns:
        feature_percentage_column = column
        break

if feature_percentage_column is not None:

    feature_summary = feature_data[
        ["Signal", feature_percentage_column]
    ].copy()

    feature_summary = feature_summary.rename(
        columns={
            feature_percentage_column:
            "Feature-Based Anomaly Percentage"
        }
    )

    # Merge both results
    final_data = pd.merge(
        risk_summary,
        feature_summary,
        on="Signal",
        how="left"
    )

else:

    print("\nFeature anomaly percentage column was not found.")

    final_data = risk_summary.copy()

# Save final comparison
final_data.to_csv(
    "final_model_comparison.csv",
    index=False
)

# Display final results
print("\nFinal Model Comparison:\n")
print(final_data.to_string(index=False))

print("\nFinal model comparison completed.")
print("Results saved to final_model_comparison.csv")

print("\nImportant:")
print("Anomaly detection identifies unusual vibration patterns.")
print("It does not confirm actual structural damage.")