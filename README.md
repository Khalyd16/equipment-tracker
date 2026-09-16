# Equipment & Maintenance Tracker

A simple menu-driven Python application for tracking engineering
equipment/tools and their maintenance history. Built as a SIWES
practical project (Weeks 19–23) to apply skills in program structure,
input validation, database design, CRUD operations, and testing.

## 1. Purpose

Small engineering teams often need a lightweight way to know:
- What equipment/tools exist and where they are
- Whether an item is available, in use, under maintenance, or retired
- A history of maintenance work done on each item

This project provides a basic, working version of that.

## 2. Features

- Add, view, update, and delete equipment records
- Log maintenance activities against a specific piece of equipment
- View maintenance history per item or across all equipment
- Input validation on all user-entered data
- Persistent storage using SQLite (data survives between runs)

## 3. System Flow

```
START
  |
  v
Show Menu
  |
  v
User selects option
  |
  v
Validate input
  |
  +-- invalid --> Show error --> back to Menu
  |
  v (valid)
Perform database operation (add / view / update / delete)
  |
  v
Show result to user
  |
  v
Back to Menu (loop until user chooses Exit)
```

## 4. Database Structure

**Table: equipment**
| Column   | Type    | Notes                                          |
|----------|---------|-------------------------------------------------|
| id       | INTEGER | Primary key, auto-increment                     |
| name     | TEXT    | Equipment name                                  |
| category | TEXT    | e.g. Tool, Machine, Instrument                  |
| status   | TEXT    | Available / In Use / Under Maintenance / Retired|
| location | TEXT    | Where the item is kept                          |

**Table: maintenance_logs**
| Column       | Type    | Notes                                  |
|--------------|---------|------------------------------------------|
| id           | INTEGER | Primary key, auto-increment              |
| equipment_id | INTEGER | Foreign key -> equipment.id              |
| date         | TEXT    | Date of maintenance (YYYY-MM-DD)         |
| description  | TEXT    | What was done                            |
| technician   | TEXT    | Who did the work                         |

The two tables are linked by `equipment_id`, so every maintenance log
belongs to exactly one piece of equipment, and deleting an equipment
record cascades to remove its logs.

## 5. File Structure

```
equipment-tracker/
├── main.py          # CLI menu and user interaction
├── database.py       # Database connection, schema, CRUD functions
├── validators.py      # Input validation helper functions
├── test_app.py        # Functional and edge-case tests
└── README.md          # This documentation
```

## 6. How to Run

Requirements: Python 3.8+ (uses only the standard library, no
external packages needed).

```bash
python main.py
```

To run the test suite:

```bash
python test_app.py
```

## 7. Usage Guide

1. Choose **1** to add a new equipment record (name, category, location).
2. Choose **2** to view all equipment in a table.
3. Choose **3** to change an item's status (e.g. mark it "Under Maintenance").
4. Choose **4** to remove an equipment record.
5. Choose **5** to log a maintenance activity against an item.
6. Choose **6** or **7** to review maintenance history.
7. Choose **0** to exit.

## 8. Known Limitations / Possible Improvements

- Single-user, command-line only (no multi-user access or GUI yet)
- No user authentication
- No report export (e.g. CSV) yet — listed as a possible future improvement
- Dates are entered automatically as "today"; no manual backdating in the current version

## 9. Concepts Applied

- Program structure and modular functions
- Input validation and error handling
- SQLite database design and CRUD operations
- Functional and edge-case testing
- Iterative debugging and code refinement
- Version control with Git (recommended: commit after each working feature)
