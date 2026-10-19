"""Command-line weather lookup with persistent favorite locations."""

import argparse
import os
from pathlib import Path
import sys

if __package__:
    from .favorites import FavoritesManager
    from .weather_api import WeatherAPI, format_current_weather, format_forecast
else:
    from favorites import FavoritesManager
    from weather_api import WeatherAPI, format_current_weather, format_forecast


FAVORITES_FILE = Path(__file__).with_name("favorites.json")


def load_api_key():
    """Prefer the environment, then the ignored config.py beside this script."""
    api_key = os.environ.get("WEATHER_API_KEY")
    if api_key:
        return api_key
    try:
        if __package__:
            from .config import WEATHER_API_KEY
        else:
            from config import WEATHER_API_KEY
    except ImportError:
        return None
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return None
    return WEATHER_API_KEY


def build_parser():
    parser = argparse.ArgumentParser(description="Look up weather and save favorite locations.")
    commands = parser.add_subparsers(dest="command", required=True)
    current = commands.add_parser("current", help="Show current weather")
    current.add_argument("location", help="Location or favorite name")
    forecast = commands.add_parser("forecast", help="Show a 1–3 day forecast")
    forecast.add_argument("location", help="Location or favorite name")
    forecast.add_argument("--days", type=int, choices=(1, 2, 3), default=3)
    favorites = commands.add_parser("favorites", help="Manage favorite locations")
    favorite_commands = favorites.add_subparsers(dest="favorites_command", required=True)
    add = favorite_commands.add_parser("add", help="Add a favorite")
    add.add_argument("name")
    add.add_argument("location")
    favorite_commands.add_parser("list", help="List favorites")
    remove = favorite_commands.add_parser("remove", help="Remove a favorite")
    remove.add_argument("name")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    favorites = FavoritesManager(FAVORITES_FILE)
    if args.command == "favorites":
        try:
            if args.favorites_command == "add":
                if not favorites.add(args.name, args.location):
                    print(f"Favorite '{args.name}' already exists.", file=sys.stderr)
                    return 1
                print(f"Added favorite '{args.name}': {args.location}")
            elif args.favorites_command == "remove":
                if not favorites.remove(args.name):
                    print(f"Favorite '{args.name}' does not exist.", file=sys.stderr)
                    return 1
                print(f"Removed favorite '{args.name}'.")
            else:
                locations = favorites.list_all()
                for name, location in sorted(locations.items()):
                    print(f"{name}: {location}")
                if not locations:
                    print("No favorites saved.")
        except OSError:
            print("Unable to save favorites. Check the file permissions.", file=sys.stderr)
            return 1
        return 0

    api_key = load_api_key()
    if not api_key:
        print("Missing API key. Set WEATHER_API_KEY or add it to week08/config.py.", file=sys.stderr)
        return 1
    location = favorites.get_location(args.location)
    if location is None:
        location = args.location
    api = WeatherAPI(api_key)
    if args.command == "current":
        data = api.get_current_weather(location)
        formatter = format_current_weather
    else:
        data = api.get_forecast(location, days=args.days)
        formatter = format_forecast
    if data is None:
        print("Unable to retrieve weather. Check the location, API key, and connection.", file=sys.stderr)
        return 1
    try:
        output = formatter(data)
    except (KeyError, TypeError):
        print("The weather service returned incomplete data.", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
