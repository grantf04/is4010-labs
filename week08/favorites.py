"""Store named weather locations in a JSON file."""

import json
from pathlib import Path


class FavoritesManager:
    """Manage persistent favorites using case-insensitive names."""

    def __init__(self, filename):
        self.filename = Path(filename)
        self._favorites = {}
        try:
            data = json.loads(self.filename.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError):
            return
        if isinstance(data, dict) and all(
            isinstance(name, str) and isinstance(location, str)
            for name, location in data.items()
        ):
            self._favorites = {name.casefold(): location for name, location in data.items()}

    def _save(self, favorites):
        self.filename.write_text(
            json.dumps(favorites, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self._favorites = favorites

    def add(self, name, location):
        """Save a new favorite, returning False if its name already exists."""
        name = name.casefold()
        if name in self._favorites:
            return False
        favorites = self._favorites.copy()
        favorites[name] = location
        self._save(favorites)
        return True

    def remove(self, name):
        """Remove a favorite, returning False if its name does not exist."""
        name = name.casefold()
        if name not in self._favorites:
            return False
        favorites = self._favorites.copy()
        del favorites[name]
        self._save(favorites)
        return True

    def list_all(self):
        """Return a copy so callers cannot change favorites without saving."""
        return self._favorites.copy()

    def get_location(self, name):
        """Return the location for a name, or None when it is unknown."""
        return self._favorites.get(name.casefold())
