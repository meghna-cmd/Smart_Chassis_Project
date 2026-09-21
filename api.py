
"""Smart Chassis Vibration Analysis API with SQLite storage."""

from datetime import datetime
from pathlib import Path
import logging
import sqlite3

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartChassisAPI")


# Application
app = FastAPI(
    title="Smart Chassis Vibration API",
    version="1.0.0"
)


# Database
DATABASE_PATH = Path("outputs") / "smart_chassis.db"
DATABASE_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    """Create a database connection."""
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the analyses table if it does not exist."""

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            samples INTEGER NOT NULL,
            mean REAL NOT NULL,
            rms REAL NOT NULL,
            standard_deviation REAL NOT NULL,
            peak_to_peak REAL NOT NULL,
            anomaly_count INTEGER NOT NULL,
            anomaly_percentage REAL NOT NULL,
            warning TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    logger.info("Database initialized successfully")


initialize_database()


# Request model
class VibrationRequest(BaseModel):
    readings: list[float] = Field(
        min_length=5,
        max_length=100000
    )


# Routes
@app.get("/")
def home():
    """API home route."""

    return {
        "message": "Smart Chassis Vibration API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    """Check API health."""

    return {
        "status": "ok",
        "service": "smart-chassis-api",
        "database": "connected"
    }


@app.post("/analyze")
def analyze(request: VibrationRequest):
    """Analyze vibration readings and save results to SQLite."""

    try:
        values = np.asarray(request.readings, dtype=float)

        if not np.isfinite(values).all():
            raise HTTPException(
                status_code=400,
                detail="Readings must be finite numbers."
            )

        mean = float(values.mean())
        rms = float(np.sqrt(np.mean(values ** 2)))
        std = float(values.std())
        peak_to_peak = float(values.max() - values.min())

        threshold = float(
            np.percentile(np.abs(values), 98)
        )

        anomaly_count = int(
            (np.abs(values) > threshold).sum()
        )

        anomaly_percentage = round(
            anomaly_count / len(values) * 100,
            2
        )

        warning = (
            "Review required"
            if anomaly_count
            else "No threshold exceedance"
        )

        created_at = datetime.now().isoformat(
            timespec="seconds"
        )

        # Save analysis in SQLite
        connection = get_connection()

        cursor = connection.execute("""
            INSERT INTO analyses (
                created_at,
                samples,
                mean,
                rms,
                standard_deviation,
                peak_to_peak,
                anomaly_count,
                anomaly_percentage,
                warning
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            created_at,
            len(values),
            mean,
            rms,
            std,
            peak_to_peak,
            anomaly_count,
            anomaly_percentage,
            warning
        ))

        analysis_id = cursor.lastrowid

        connection.commit()
        connection.close()

        logger.info(
            "Analysis saved successfully: id=%s",
            analysis_id
        )

        return {
            "analysis_id": analysis_id,
            "created_at": created_at,
            "samples": int(len(values)),
            "mean": round(mean, 6),
            "rms": round(rms, 6),
            "standard_deviation": round(std, 6),
            "peak_to_peak": round(peak_to_peak, 6),
            "anomaly_count": anomaly_count,
            "anomaly_percentage": anomaly_percentage,
            "warning": warning,
            "database_saved": True
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception(
            "Analysis failed: %s",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during analysis."
        )


@app.get("/analyses")
def get_analyses():
    """Return the latest saved analyses."""

    connection = get_connection()

    rows = connection.execute("""
        SELECT
            id,
            created_at,
            samples,
            mean,
            rms,
            standard_deviation,
            peak_to_peak,
            anomaly_count,
            anomaly_percentage,
            warning
        FROM analyses
        ORDER BY id DESC
        LIMIT 20
    """).fetchall()

    connection.close()

    columns = [
        "id",
        "created_at",
        "samples",
        "mean",
        "rms",
        "standard_deviation",
        "peak_to_peak",
        "anomaly_count",
        "anomaly_percentage",
        "warning"
    ]

    results = [
        dict(zip(columns, row))
        for row in rows
    ]

    return {
        "count": len(results),
        "analyses": results
    }