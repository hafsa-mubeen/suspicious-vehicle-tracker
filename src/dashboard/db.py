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
            video_source TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_alert(timestamp, person_id, vehicle_id, roi_id, snapshot_path, video_source):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO alerts (timestamp, person_id, vehicle_id, roi_id, snapshot_path, video_source) VALUES (?, ?, ?, ?, ?, ?)",
        (timestamp, person_id, vehicle_id, roi_id, snapshot_path, video_source)
    )
    conn.commit()
    conn.close()


def get_all_alerts():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT * FROM alerts ORDER BY timestamp DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def clear_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM alerts")
    conn.commit()
    conn.close()