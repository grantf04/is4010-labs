def find_common_elements(list1, list2):
    """Return a list of values present in both input lists."""
    return list(set(list1) & set(list2))


def find_user_by_name(users, name):
    """Return the matching user dictionary, or None when no user matches."""
    for user in users:
        if user["name"] == name:
            return user
    return None


def get_list_of_even_numbers(numbers):
    """Return the even integers in their original order."""
    return [number for number in numbers if number % 2 == 0]
