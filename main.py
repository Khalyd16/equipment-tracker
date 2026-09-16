"""
main.py
Equipment & Maintenance Tracker
A menu-driven CLI application for tracking engineering equipment and
its maintenance history.

Run with: python main.py
"""

import database as db
import validators as v


def print_menu():
    print("\n===== Equipment & Maintenance Tracker =====")
    print("1. Add new equipment")
    print("2. View all equipment")
    print("3. Update equipment status")
    print("4. Delete equipment")
    print("5. Log a maintenance activity")
    print("6. View maintenance logs for an equipment")
    print("7. View all maintenance logs")
    print("0. Exit")


def add_equipment_flow():
    print("\n-- Add New Equipment --")
    name = input("Equipment name: ").strip()
    if not v.is_non_empty(name):
        print("Error: Equipment name cannot be empty.")
        return

    category = input("Category (e.g. Tool, Machine, Instrument): ").strip()
    if not v.is_non_empty(category):
        print("Error: Category cannot be empty.")
        return

    location = input("Location: ").strip()
    if not v.is_non_empty(location):
        print("Error: Location cannot be empty.")
        return

    new_id = db.add_equipment(name, category, location)
    print(f"Equipment added successfully with ID {new_id}.")


def view_equipment_flow():
    print("\n-- All Equipment --")
    rows = db.get_all_equipment()
    if not rows:
        print("No equipment records found.")
        return
    print(f"{'ID':<5}{'Name':<20}{'Category':<15}{'Status':<18}{'Location':<15}")
    print("-" * 73)
    for row in rows:
        eq_id, name, category, status, location = row
        print(f"{eq_id:<5}{name:<20}{category:<15}{status:<18}{location:<15}")


def update_status_flow():
    print("\n-- Update Equipment Status --")
    eq_id = input("Equipment ID: ").strip()
    if not v.is_valid_id(eq_id):
        print("Error: Please enter a valid positive integer ID.")
        return

    record = db.get_equipment_by_id(int(eq_id))
    if record is None:
        print(f"Error: No equipment found with ID {eq_id}.")
        return

    print(f"Current status: {record[3]}")
    print(f"Valid statuses: {', '.join(sorted(v.VALID_STATUSES))}")
    new_status = input("New status: ").strip()
    if not v.is_valid_status(new_status):
        print("Error: Invalid status entered.")
        return

    db.update_equipment_status(int(eq_id), new_status)
    print("Status updated successfully.")


def delete_equipment_flow():
    print("\n-- Delete Equipment --")
    eq_id = input("Equipment ID to delete: ").strip()
    if not v.is_valid_id(eq_id):
        print("Error: Please enter a valid positive integer ID.")
        return

    record = db.get_equipment_by_id(int(eq_id))
    if record is None:
        print(f"Error: No equipment found with ID {eq_id}.")
        return

    confirm = input(f"Are you sure you want to delete '{record[1]}'? (y/n): ").strip().lower()
    if confirm == "y":
        db.delete_equipment(int(eq_id))
        print("Equipment deleted.")
    else:
        print("Deletion cancelled.")


def add_log_flow():
    print("\n-- Log Maintenance Activity --")
    eq_id = input("Equipment ID: ").strip()
    if not v.is_valid_id(eq_id):
        print("Error: Please enter a valid positive integer ID.")
        return

    record = db.get_equipment_by_id(int(eq_id))
    if record is None:
        print(f"Error: No equipment found with ID {eq_id}.")
        return

    description = input("Description of work done: ").strip()
    if not v.is_non_empty(description):
        print("Error: Description cannot be empty.")
        return

    technician = input("Technician name: ").strip()
    if not v.is_non_empty(technician):
        print("Error: Technician name cannot be empty.")
        return

    db.add_maintenance_log(int(eq_id), description, technician)
    print("Maintenance log added successfully.")


def view_logs_for_equipment_flow():
    print("\n-- Maintenance Logs for Equipment --")
    eq_id = input("Equipment ID: ").strip()
    if not v.is_valid_id(eq_id):
        print("Error: Please enter a valid positive integer ID.")
        return

    logs = db.get_logs_for_equipment(int(eq_id))
    if not logs:
        print("No maintenance logs found for this equipment.")
        return

    for log in logs:
        log_id, _, date, description, technician = log
        print(f"[{date}] {description} (by {technician})")


def view_all_logs_flow():
    print("\n-- All Maintenance Logs --")
    logs = db.get_all_logs()
    if not logs:
        print("No maintenance logs found.")
        return

    for log in logs:
        _, equipment_name, date, description, technician = log
        print(f"[{date}] {equipment_name}: {description} (by {technician})")


def main():
    db.initialize_database()

    actions = {
        "1": add_equipment_flow,
        "2": view_equipment_flow,
        "3": update_status_flow,
        "4": delete_equipment_flow,
        "5": add_log_flow,
        "6": view_logs_for_equipment_flow,
        "7": view_all_logs_flow,
    }

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Exiting. Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
