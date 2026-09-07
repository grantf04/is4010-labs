"""Small functions for the Lab 02 CLI-agent comparison."""


def make_greeting(name: str) -> str:
    """Return exactly 'Hello, NAME!' using the supplied name."""
    return f"Hello, {name}!"


def is_even(number: int) -> bool:
    """Return True when number is even and False otherwise."""
    return number % 2 == 0


def count_vowels(text: str) -> int:
    """Count a, e, i, o, and u without regard to case; do not count y."""
    return sum(character in "aeiou" for character in text.lower())
