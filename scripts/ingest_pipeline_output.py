import sys
sys.path.insert(0, ".")
import json
from src.dashboard.db import init_db, insert_alert

def ingest(output_file):
    init_db()
    count = 0
    with open(output_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("{") and "timestamp" in line:
                try:
                    alert = json.loads(line)
                    insert_alert(
                        timestamp=alert["timestamp"],
                        person_id=int(alert["person_id"]),
                        vehicle_id=int(alert["vehicle_id"]),
                        roi_id=alert["roi_id"],
                        snapshot_path=alert.get("snapshot_path", "unknown.jpg"),
                        video_source=alert.get("video_source", "unknown.mp4")
                    )
                    count += 1
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Skipped malformed line: {e}")
    print(f"Ingested {count} alerts from {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest_pipeline_output.py <output_file>")
        sys.exit(1)
    ingest(sys.argv[1])