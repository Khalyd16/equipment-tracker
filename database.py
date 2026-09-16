"""
database.py
Handles all database setup and CRUD (Create, Read, Update, Delete) operations
for the Equipment & Maintenance Tracker.
"""

import sqlite3
from datetime import datetime

DB_NAME = "equipment_tracker.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create the equipment and maintenance_logs tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available',
            location TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            technician TEXT NOT NULL,
            FOREIGN KEY (equipment_id) REFERENCES equipment (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ---------- Equipment CRUD ----------

def add_equipment(name, category, location, status="Available"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO equipment (name, category, status, location) VALUES (?, ?, ?, ?)",
        (name, category, status, location)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_equipment():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipment")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_equipment_by_id(equipment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_equipment_status(equipment_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE equipment SET status = ? WHERE id = ?",
        (new_status, equipment_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0


def delete_equipment(equipment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0


# ---------- Maintenance Log CRUD ----------

def add_maintenance_log(equipment_id, description, technician, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO maintenance_logs (equipment_id, date, description, technician) VALUES (?, ?, ?, ?)",
        (equipment_id, date, description, technician)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_logs_for_equipment(equipment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM maintenance_logs WHERE equipment_id = ?", (equipment_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT maintenance_logs.id, equipment.name, maintenance_logs.date,
               maintenance_logs.description, maintenance_logs.technician
        FROM maintenance_logs
        JOIN equipment ON maintenance_logs.equipment_id = equipment.id
        ORDER BY maintenance_logs.date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
