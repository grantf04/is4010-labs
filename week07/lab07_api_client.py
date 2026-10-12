"""Fetch JSON data from an HTTP API with basic error handling."""

import requests


def get_api_data(url):
    """Return parsed JSON from url, or None when the request or decoding fails."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError):
        return None
