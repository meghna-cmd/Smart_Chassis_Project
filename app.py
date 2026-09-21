import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from logging_config import logger
from error_handler import handle_error

from project_config import (
    PERCENTILE_THRESHOLD,
    DATASET_FILE,
    FEATURE_FILE,
    ML_RESULT_FILE,
    COMPARISON_FILE
)

from realtime_sensor import collect_readings


# ==================================================
# PAGE CONFIGURATION
# ==================================================

logger.info("Smart Chassis dashboard started")

st.set_page_config(
    page_title="Smart Chassis Vibration Analysis",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Smart Chassis Vibration Analysis System")

st.write(
    "A prototype system for vibration analysis, "
    "anomaly detection and potential structural-risk indication."
)

st.info(
    "Important: Unusual vibration does not confirm a real crack. "
    "This project is a prototype and requires real-world validation."
)


# ==================================================
# LOAD DATASET
# ==================================================

@st.cache_data
def load_dataset():

    file_path = Path(DATASET_FILE)

    if not file_path.exists():

        logger.error("Dataset not found: %s", file_path)

        st.error(
            f"Dataset not found: {DATASET_FILE}"
        )

        st.stop()

    raw_data = pd.read_excel(
        file_path,
        header=None
    )

    data = raw_data.iloc[5:, 2:].copy()

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

    data = data.apply(
        pd.to_numeric,
        errors="coerce"
    )

    logger.info(
        "Dataset loaded successfully: rows=%s, columns=%s",
        data.shape[0],
        data.shape[1]
    )

    return data


data = load_dataset()


# ==================================================
# SIDEBAR CONTROLS
# ==================================================

st.sidebar.header("⚙️ Project Controls")

selected_signal = st.sidebar.selectbox(
    "Select Vibration Signal",
    data.columns
)

st.sidebar.write(
    f"Percentile Threshold: {PERCENTILE_THRESHOLD}%"
)


# ==================================================
# REAL-TIME SENSOR CONTROLS
# ==================================================

st.sidebar.divider()

st.sidebar.header("📡 Sensor Simulation")

enable_sensor = st.sidebar.checkbox(
    "Enable Real-Time Sensor Simulator",
    value=False
)

sensor_duration = st.sidebar.slider(
    "Simulation Duration (seconds)",
    min_value=1,
    max_value=30,
    value=5
)

sensor_sample_rate = st.sidebar.slider(
    "Sensor Sample Rate (Hz)",
    min_value=10,
    max_value=200,
    value=100
)

sensor_anomaly_probability = st.sidebar.slider(
    "Anomaly Probability",
    min_value=0.0,
    max_value=0.20,
    value=0.02,
    step=0.01
)


# ==================================================
# REAL-TIME SENSOR SIMULATION
# ==================================================

if enable_sensor:

    st.header("📡 Real-Time Vibration Sensor Simulation")

    st.caption(
        "This section uses simulated accelerometer data. "
        "It is not connected to a physical sensor."
    )

    try:

        readings = collect_readings(
            sample_rate=float(sensor_sample_rate),
            duration=float(sensor_duration),
            base_frequency=5.0,
            noise_level=0.15,
            anomaly_probability=float(
                sensor_anomaly_probability
            ),
            seed=42
        )

        sensor_data = pd.DataFrame({

            "Timestamp": [
                reading.timestamp
                for reading in readings
            ],

            "Acceleration": [
                reading.acceleration
                for reading in readings
            ],

            "Anomaly": [
                reading.anomaly
                for reading in readings
            ]

        })

        sensor_signal = sensor_data[
            "Acceleration"
        ].to_numpy()

        sensor_anomaly_count = int(
            sensor_data["Anomaly"].sum()
        )

        sensor_total_samples = len(
            sensor_data
        )

        sensor_anomaly_percentage = (
            sensor_anomaly_count
            / sensor_total_samples
            * 100
        )

        sensor_col1, sensor_col2, sensor_col3 = (
            st.columns(3)
        )

        with sensor_col1:

            st.metric(
                "Sensor Samples",
                sensor_total_samples
            )

        with sensor_col2:

            st.metric(
                "Simulated Anomalies",
                sensor_anomaly_count
            )

        with sensor_col3:

            st.metric(
                "Anomaly Percentage",
                f"{sensor_anomaly_percentage:.2f}%"
            )

        st.subheader(
            "📈 Simulated Sensor Vibration"
        )

        sensor_chart_data = sensor_data[
            ["Timestamp", "Acceleration"]
        ].set_index("Timestamp")

        st.line_chart(
            sensor_chart_data
        )

        st.subheader(
            "🚨 Sensor Anomaly Timeline"
        )

        sensor_anomaly_data = sensor_data.copy()

        sensor_anomaly_data[
            "Detected Anomaly"
        ] = np.where(
            sensor_anomaly_data["Anomaly"],
            sensor_anomaly_data["Acceleration"],
            np.nan
        )

        st.line_chart(
            sensor_anomaly_data.set_index(
                "Timestamp"
            )[
                [
                    "Acceleration",
                    "Detected Anomaly"
                ]
            ]
        )

        st.subheader(
            "📋 Sensor Data Preview"
        )

        st.dataframe(
            sensor_data,
            use_container_width=True
        )

        sensor_csv = sensor_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Simulated Sensor Data",
            data=sensor_csv,
            file_name="simulated_sensor_data.csv",
            mime="text/csv"
        )

        logger.info(
            "Sensor simulation completed: samples=%s, anomalies=%s",
            sensor_total_samples,
            sensor_anomaly_count
        )

        st.success(
            "Sensor simulation completed successfully."
        )

    except Exception as error:

        handle_error(
            error,
            "Real-Time Sensor Simulation"
        )

        st.error(
            "Sensor simulation failed. "
            "Check outputs/application.log for details."
        )


# ==================================================
# SIGNAL PREPARATION
# ==================================================

selected_data = data[selected_signal]

missing_values = int(
    selected_data.isna().sum()
)

signal = selected_data.dropna().to_numpy()

if len(signal) == 0:

    st.error(
        "Selected signal contains no valid samples."
    )

    st.stop()

absolute_signal = np.abs(signal)

sample_numbers = np.arange(
    len(signal)
)

mean_value = np.mean(signal)

rms_value = np.sqrt(
    np.mean(signal ** 2)
)

std_value = np.std(signal)

peak_to_peak = np.ptp(signal)

maximum_value = np.max(
    absolute_signal
)

if rms_value != 0:

    crest_factor = (
        maximum_value / rms_value
    )

else:

    crest_factor = 0


# ==================================================
# DATASET INFORMATION
# ==================================================

st.header("📁 Dataset Information")

info_col1, info_col2, info_col3, info_col4 = (
    st.columns(4)
)

with info_col1:

    st.metric(
        "Selected Signal",
        selected_signal
    )

with info_col2:

    st.metric(
        "Valid Samples",
        len(signal)
    )

with info_col3:

    st.metric(
        "Missing Values",
        missing_values
    )

with info_col4:

    st.metric(
        "Total Signals",
        len(data.columns)
    )


# ==================================================
# VIBRATION FEATURES
# ==================================================

st.header("📊 Vibration Features")

feature_col1, feature_col2, feature_col3, feature_col4 = (
    st.columns(4)
)

with feature_col1:

    st.metric(
        "RMS",
        f"{rms_value:.4f}"
    )

with feature_col2:

    st.metric(
        "Standard Deviation",
        f"{std_value:.4f}"
    )

with feature_col3:

    st.metric(
        "Peak-to-Peak",
        f"{peak_to_peak:.4f}"
    )

with feature_col4:

    st.metric(
        "Crest Factor",
        f"{crest_factor:.4f}"
    )

st.write(
    f"Mean Acceleration: **{mean_value:.4f}**"
)


# ==================================================
# TIME-DOMAIN ANALYSIS
# ==================================================

st.header(
    "📉 Time-Domain Vibration Analysis"
)

time_domain_data = pd.DataFrame({

    "Sample": sample_numbers,

    "Acceleration": signal

})

st.line_chart(
    time_domain_data.set_index(
        "Sample"
    )
)
# ==================================================
# STATISTICAL ANOMALY DETECTION
# ==================================================

st.header(
    "🚨 Statistical Anomaly Detection"
)

statistical_threshold = np.percentile(
    absolute_signal,
    PERCENTILE_THRESHOLD
)

statistical_anomaly_mask = (
    absolute_signal > statistical_threshold
)

statistical_anomaly_count = int(
    np.sum(statistical_anomaly_mask)
)

statistical_anomaly_percentage = (
    statistical_anomaly_count / len(signal)
) * 100


stat_col1, stat_col2, stat_col3 = (
    st.columns(3)
)

with stat_col1:

    st.metric(
        "Anomaly Threshold",
        f"{statistical_threshold:.4f}"
    )

with stat_col2:

    st.metric(
        "Anomaly Count",
        statistical_anomaly_count
    )

with stat_col3:

    st.metric(
        "Anomaly Percentage",
        f"{statistical_anomaly_percentage:.2f}%"
    )


# ==================================================
# WARNING SYSTEM
# ==================================================

st.subheader(
    "⚠️ Warning Status"
)

if statistical_anomaly_percentage > 7:

    st.error(
        "HIGH WARNING: Unusual vibration pattern detected."
    )

elif statistical_anomaly_percentage >= 5:

    st.warning(
        "MEDIUM WARNING: Vibration pattern requires monitoring."
    )

else:

    st.success(
        "LOW WARNING: Low statistical anomaly percentage."
    )

st.caption(
    "Warning thresholds are prototype values and "
    "have not been industrially validated."
)


# ==================================================
# ANOMALY TIMELINE
# ==================================================

st.subheader(
    "🔎 Anomaly Timeline"
)

anomaly_values = np.where(
    statistical_anomaly_mask,
    signal,
    np.nan
)

anomaly_timeline_data = pd.DataFrame({

    "Sample": sample_numbers,

    "Original Signal": signal,

    "Detected Anomaly": anomaly_values

})

st.line_chart(
    anomaly_timeline_data.set_index(
        "Sample"
    )
)


# ==================================================
# FREQUENCY-DOMAIN ANALYSIS
# ==================================================

st.header(
    "🌊 Frequency-Domain Analysis"
)

centered_signal = (
    signal - np.mean(signal)
)

fft_values = np.fft.rfft(
    centered_signal
)

frequency_values = np.fft.rfftfreq(
    len(centered_signal)
)

magnitude_values = np.abs(
    fft_values
)

if len(magnitude_values) > 1:

    dominant_index = (
        np.argmax(
            magnitude_values[1:]
        ) + 1
    )

else:

    dominant_index = 0


dominant_frequency_index = (
    frequency_values[dominant_index]
)

dominant_magnitude = (
    magnitude_values[dominant_index]
)


freq_col1, freq_col2 = (
    st.columns(2)
)

with freq_col1:

    st.metric(
        "Dominant Frequency Index",
        f"{dominant_frequency_index:.6f}"
    )

with freq_col2:

    st.metric(
        "Dominant Magnitude",
        f"{dominant_magnitude:.4f}"
    )


frequency_data = pd.DataFrame({

    "Frequency Index": frequency_values,

    "Magnitude": magnitude_values

})

st.line_chart(
    frequency_data.set_index(
        "Frequency Index"
    )
)

st.caption(
    "The sampling rate is unavailable. Therefore, "
    "frequency is displayed as a normalized index, not Hz."
)


# ==================================================
# ALL SIGNALS SUMMARY
# ==================================================

st.header(
    "📋 All Signals Summary"
)

summary_rows = []

for column in data.columns:

    current_series = data[column].dropna()

    if len(current_series) == 0:

        continue

    current_signal = (
        current_series.to_numpy()
    )

    current_absolute = np.abs(
        current_signal
    )

    current_rms = np.sqrt(
        np.mean(current_signal ** 2)
    )

    current_std = np.std(
        current_signal
    )

    current_peak_to_peak = np.ptp(
        current_signal
    )

    if current_rms != 0:

        current_crest_factor = (
            np.max(current_absolute)
            / current_rms
        )

    else:

        current_crest_factor = 0

    current_threshold = np.percentile(
        current_absolute,
        PERCENTILE_THRESHOLD
    )

    current_anomaly_count = np.sum(
        current_absolute > current_threshold
    )

    current_anomaly_percentage = (
        current_anomaly_count
        / len(current_signal)
    ) * 100

    summary_rows.append({

        "Signal": column,

        "Samples": len(current_signal),

        "RMS": round(
            current_rms,
            4
        ),

        "Standard Deviation": round(
            current_std,
            4
        ),

        "Peak-to-Peak": round(
            current_peak_to_peak,
            4
        ),

        "Crest Factor": round(
            current_crest_factor,
            4
        ),

        "Anomaly Percentage": round(
            current_anomaly_percentage,
            2
        )

    })


summary_df = pd.DataFrame(
    summary_rows
)

st.dataframe(
    summary_df,
    use_container_width=True
)


# ==================================================
# RMS COMPARISON
# ==================================================

st.subheader(
    "📊 RMS Comparison Across Signals"
)

rms_comparison = summary_df[
    [
        "Signal",
        "RMS"
    ]
].set_index(
    "Signal"
)

st.bar_chart(
    rms_comparison
)


# ==================================================
# STANDARD DEVIATION COMPARISON
# ==================================================

st.subheader(
    "📊 Standard Deviation Comparison"
)

std_comparison = summary_df[
    [
        "Signal",
        "Standard Deviation"
    ]
].set_index(
    "Signal"
)

st.bar_chart(
    std_comparison
)


# ==================================================
# PEAK-TO-PEAK COMPARISON
# ==================================================

st.subheader(
    "📊 Peak-to-Peak Comparison"
)

peak_comparison = summary_df[
    [
        "Signal",
        "Peak-to-Peak"
    ]
].set_index(
    "Signal"
)

st.bar_chart(
    peak_comparison
)
# ==================================================
# HELPER FUNCTION
# ==================================================

def filter_by_selected_signal(
    dataframe,
    selected_signal
):

    possible_columns = [
        "Signal",
        "signal",
        "Signal_Name",
        "signal_name",
        "Vibration_Signal",
        "vibration_signal"
    ]

    found_column = None

    for column in possible_columns:

        if column in dataframe.columns:

            found_column = column
            break

    if found_column is None:

        return dataframe, False

    filtered_data = dataframe[
        dataframe[found_column].astype(str)
        == str(selected_signal)
    ].copy()

    if filtered_data.empty:

        return dataframe, False

    return filtered_data, True


# ==================================================
# FREQUENCY FEATURES
# ==================================================

st.header(
    "🔬 Frequency Features"
)

frequency_file = Path(
    FEATURE_FILE
)

if frequency_file.exists():

    try:

        frequency_features = pd.read_csv(
            frequency_file
        )

        filtered_frequency_features, is_filtered = (
            filter_by_selected_signal(
                frequency_features,
                selected_signal
            )
        )

        if is_filtered:

            st.info(
                f"Showing frequency features for "
                f"{selected_signal}"
            )

            st.dataframe(
                filtered_frequency_features,
                use_container_width=True
            )

        else:

            st.info(
                "Signal name was not found in the file. "
                "Complete frequency-feature dataset is displayed."
            )

            st.dataframe(
                frequency_features,
                use_container_width=True
            )

    except Exception as error:

        handle_error(
            error,
            "Frequency Features"
        )

        st.error(
            "Unable to load frequency features."
        )

else:

    st.warning(
        "frequency_features.csv was not found."
    )


# ==================================================
# MACHINE LEARNING RESULTS
# ==================================================

st.header(
    "🤖 Machine Learning Anomaly Results"
)

ml_file = Path(
    ML_RESULT_FILE
)

if ml_file.exists():

    try:

        ml_results = pd.read_csv(
            ml_file
        )

        filtered_ml_results, is_filtered = (
            filter_by_selected_signal(
                ml_results,
                selected_signal
            )
        )

        if is_filtered:

            displayed_ml_results = (
                filtered_ml_results
            )

            st.info(
                f"Showing machine-learning results "
                f"for {selected_signal}"
            )

        else:

            displayed_ml_results = ml_results

            st.info(
                "Signal name was not found in the ML file. "
                "Complete ML dataset is displayed."
            )

        st.dataframe(
            displayed_ml_results,
            use_container_width=True
        )

        st.subheader(
            "Machine Learning Result Summary"
        )

        numeric_columns = (
            displayed_ml_results.select_dtypes(
                include="number"
            ).columns
        )

        if len(numeric_columns) > 0:

            st.bar_chart(
                displayed_ml_results[
                    numeric_columns
                ]
            )

        else:

            st.info(
                "No numeric ML columns are available."
            )

    except Exception as error:

        handle_error(
            error,
            "Machine Learning Results"
        )

        st.error(
            "Unable to load machine learning results."
        )

else:

    st.warning(
        "ml_anomaly_results.csv was not found."
    )


# ==================================================
# FINAL MODEL COMPARISON
# ==================================================

st.header(
    "⚖️ Final Model Comparison"
)

comparison_file = Path(
    COMPARISON_FILE
)

if comparison_file.exists():

    try:

        comparison_data = pd.read_csv(
            comparison_file
        )

        filtered_comparison_data, is_filtered = (
            filter_by_selected_signal(
                comparison_data,
                selected_signal
            )
        )

        if is_filtered:

            displayed_comparison_data = (
                filtered_comparison_data
            )

            st.info(
                f"Showing model comparison for "
                f"{selected_signal}"
            )

        else:

            displayed_comparison_data = (
                comparison_data
            )

            st.caption(
                "Final Model Comparison is a global "
                "comparison of models."
            )

        st.dataframe(
            displayed_comparison_data,
            use_container_width=True
        )

    except Exception as error:

        handle_error(
            error,
            "Final Model Comparison"
        )

        st.error(
            "Unable to load final model comparison."
        )

else:

    st.warning(
        "final_model_comparison.csv was not found."
    )


# ==================================================
# DATA QUALITY INFORMATION
# ==================================================

st.header(
    "🔍 Data Quality Information"
)

quality_col1, quality_col2, quality_col3 = (
    st.columns(3)
)

with quality_col1:

    st.metric(
        "Dataset Rows",
        data.shape[0]
    )

with quality_col2:

    st.metric(
        "Dataset Columns",
        data.shape[1]
    )

with quality_col3:

    st.metric(
        "Total Missing Values",
        int(
            data.isna().sum().sum()
        )
    )

st.write(
    "Missing values are handled by dropping invalid "
    "samples from the selected signal during analysis."
)


# ==================================================
# CSV DOWNLOAD
# ==================================================

st.header(
    "⬇️ Download Analysis Summary"
)

summary_csv = summary_df.to_csv(
    index=False
).encode(
    "utf-8"
)

st.download_button(
    label="Download Signal Summary CSV",
    data=summary_csv,
    file_name="signal_summary.csv",
    mime="text/csv"
)


# ==================================================
# PROJECT LIMITATIONS
# ==================================================

st.header(
    "⚠️ Project Limitations"
)

st.markdown("""
- The dataset sampling rate is unavailable.
- Frequency values are normalized frequency indices.
- Statistical anomaly detection uses a percentile-based threshold.
- Anomaly detection does not prove the presence of a real crack.
- Warning thresholds are prototype values.
- The current dataset does not provide verified structural-damage labels.
- Real-world testing and labelled vibration data are required.
- Machine learning results should not be interpreted as validated crack-prediction accuracy.
- The real-time sensor section currently uses simulated data.
- Physical accelerometer integration is not yet implemented.
""")


# ==================================================
# PROJECT CONCLUSION
# ==================================================

st.header(
    "✅ Project Conclusion"
)

st.write(
    "The system analyzes chassis vibration signals "
    "using time-domain features, frequency-domain "
    "analysis, statistical anomaly detection and "
    "machine learning results."
)

st.write(
    "A simulated sensor stream is also available "
    "for testing real-time vibration visualization."
)

st.write(
    "The prototype can support early investigation "
    "of unusual vibration patterns, but further "
    "validation is required before practical safety deployment."
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Smart Chassis Vibration Analysis System | Prototype"
)

logger.info(
    "Smart Chassis dashboard completed successfully"
)