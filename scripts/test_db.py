import sys
sys.path.insert(0, ".")

import os
import pytest
from src.dashboard.db import init_db, insert_alert, get_all_alerts, DB_PATH


@pytest.fixture
def temp_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def test_init_db_creates_table(temp_db):
    alerts = get_all_alerts()
    assert alerts == []


def test_insert_and_retrieve_alert(temp_db):
    insert_alert(
        timestamp=12.4,
        person_id=3,
        vehicle_id=7,
        roi_id=0,
        snapshot_path="snap.jpg",
        video_source="clip_01.mp4"
    )
    alerts = get_all_alerts()
    assert len(alerts) == 1
    assert alerts[0][1] == 12.4
    assert alerts[0][2] == 3
    assert alerts[0][3] == 7


def test_alerts_ordered_by_timestamp_desc(temp_db):
    insert_alert(10.0, 1, 1, 0, "a.jpg", "clip.mp4")
    insert_alert(50.0, 2, 2, 0, "b.jpg", "clip.mp4")
    insert_alert(30.0, 3, 3, 0, "c.jpg", "clip.mp4")

    alerts = get_all_alerts()
    timestamps = [a[1] for a in alerts]
    assert timestamps == [50.0, 30.0, 10.0]


def test_multiple_inserts_increment_id(temp_db):
    insert_alert(1.0, 1, 1, 0, "a.jpg", "clip.mp4")
    insert_alert(2.0, 2, 2, 0, "b.jpg", "clip.mp4")

    alerts = get_all_alerts()
    ids = sorted(a[0] for a in alerts)
    assert ids == [1, 2]