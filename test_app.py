"""
test_app.py
Manual/functional test cases for the Equipment & Maintenance Tracker.
These cover normal operation and edge cases (invalid input, missing
records, etc.) — the kind of testing described in Weeks 21 and 22.

Run with: python test_app.py
"""

import os
import database as db
import validators as v

TEST_DB = "test_equipment_tracker.db"


def setup_test_db():
    # Point the database module at a throwaway test database
    db.DB_NAME = TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db.initialize_database()


def teardown_test_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_and_retrieve_equipment():
    eq_id = db.add_equipment("Digital Multimeter", "Instrument", "Lab A")
    record = db.get_equipment_by_id(eq_id)
    assert record is not None, "Equipment should be retrievable after adding"
    assert record[1] == "Digital Multimeter"
    print("PASS: test_add_and_retrieve_equipment")


def test_update_status():
    eq_id = db.add_equipment("Drill Machine", "Tool", "Workshop")
    updated = db.update_equipment_status(eq_id, "Under Maintenance")
    record = db.get_equipment_by_id(eq_id)
    assert updated is True
    assert record[3] == "Under Maintenance"
    print("PASS: test_update_status")


def test_update_status_invalid_id():
    # Edge case: updating an ID that does not exist should not crash,
    # and should report that nothing was updated.
    updated = db.update_equipment_status(9999, "Available")
    assert updated is False
    print("PASS: test_update_status_invalid_id")


def test_delete_equipment():
    eq_id = db.add_equipment("Spare Cable", "Consumable", "Store Room")
    deleted = db.delete_equipment(eq_id)
    record = db.get_equipment_by_id(eq_id)
    assert deleted is True
    assert record is None
    print("PASS: test_delete_equipment")


def test_add_maintenance_log():
    eq_id = db.add_equipment("Oscilloscope", "Instrument", "Lab B")
    log_id = db.add_maintenance_log(eq_id, "Calibration check", "J. Bello", "2026-05-10")
    logs = db.get_logs_for_equipment(eq_id)
    assert len(logs) == 1
    assert logs[0][3] == "Calibration check"
    print("PASS: test_add_maintenance_log")


def test_validators_reject_bad_input():
    # Edge cases identified during Week 21/22 debugging
    assert v.is_non_empty("") is False
    assert v.is_non_empty("   ") is False
    assert v.is_non_empty("Valid Name") is True

    assert v.is_valid_id("abc") is False
    assert v.is_valid_id("-5") is False
    assert v.is_valid_id("12") is True

    assert v.is_valid_status("Broken") is False
    assert v.is_valid_status("Available") is True
    print("PASS: test_validators_reject_bad_input")


def run_all_tests():
    setup_test_db()
    try:
        test_add_and_retrieve_equipment()
        test_update_status()
        test_update_status_invalid_id()
        test_delete_equipment()
        test_add_maintenance_log()
        test_validators_reject_bad_input()
        print("\nAll tests passed.")
    finally:
        teardown_test_db()


if __name__ == "__main__":
    run_all_tests()
