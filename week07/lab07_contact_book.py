"""Save and load a contact book using JSON files."""

import json


def save_contacts_to_json(contacts, filename):
    """Write the contacts list to filename as indented JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def load_contacts_from_json(filename):
    """Return contacts from filename, or an empty list if it does not exist."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
