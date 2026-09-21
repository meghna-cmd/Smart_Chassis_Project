"""SQLite persistence layer for analysis summaries."""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("outputs/smart_chassis.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            signal TEXT NOT NULL,
            rms REAL,
            standard_deviation REAL,
            peak_to_peak REAL,
            anomaly_percentage REAL,
            risk_level TEXT
        )""")
        conn.commit()

def save_analysis(signal, rms, standard_deviation, peak_to_peak,
                  anomaly_percentage, risk_level):
    initialize_database()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO analyses
            (created_at, signal, rms, standard_deviation, peak_to_peak,
             anomaly_percentage, risk_level)
             VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (datetime.utcnow().isoformat(), signal, rms, standard_deviation,
             peak_to_peak, anomaly_percentage, risk_level)
        )
        conn.commit()

if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at {DB_PATH}")
