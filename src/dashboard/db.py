import sqlite3

DB_PATH = "results/alerts.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            person_id INTEGER,
            vehicle_id INTEGER,
            roi_id INTEGER,
            snapshot_path TEXT,
            video_source TEXT,
            rule_triggered TEXT,
            dwell_time_at_trigger REAL
        )
    """)
    # Migrate DBs created before these columns existed (e.g. your current alerts.db)
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(alerts)").fetchall()}
    if "rule_triggered" not in existing_cols:
        conn.execute("ALTER TABLE alerts ADD COLUMN rule_triggered TEXT")
    if "dwell_time_at_trigger" not in existing_cols:
        conn.execute("ALTER TABLE alerts ADD COLUMN dwell_time_at_trigger REAL")
    conn.commit()
    conn.close()


def insert_alert(timestamp, person_id, vehicle_id, roi_id, snapshot_path, video_source,
                  rule_triggered=None, dwell_time_at_trigger=None):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO alerts
           (timestamp, person_id, vehicle_id, roi_id, snapshot_path, video_source, rule_triggered, dwell_time_at_trigger)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (timestamp, person_id, vehicle_id, roi_id, snapshot_path, video_source, rule_triggered, dwell_time_at_trigger)
    )
    conn.commit()
    conn.close()


def get_all_alerts():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def clear_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()