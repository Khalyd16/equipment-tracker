"""
validators.py
Small helper functions for validating user input before it reaches the
database layer. Keeping these separate makes the code easier to read,
test, and maintain
"""

VALID_STATUSES = {"Available", "In Use", "Under Maintenance", "Retired"}


def is_non_empty(text):
    """Return True if text is a non-empty, non-whitespace string."""
    return isinstance(text, str) and text.strip() != ""


def is_valid_status(status):
    """Return True if status is one of the allowed equipment statuses."""
    return status in VALID_STATUSES


def is_valid_id(value):
    """Return True if value can be parsed as a positive integer ID."""
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False


def is_valid_date(date_str):
    """Very light check that a date string looks like YYYY-MM-DD."""
    import re
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))
