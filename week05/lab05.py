def calculate_average_age(users):
    """Return the average of integer and float ages, or 0.0 if none exist."""
    ages = []
    for user in users:
        age = user.get("age")
        if isinstance(age, (int, float)):
            ages.append(age)

    if not ages:
        return 0.0
    return sum(ages) / len(ages)


def get_active_user_emails(users):
    """Return existing email values for users whose is_active value is truthy."""
    emails = []
    for user in users:
        if user.get("is_active") and "email" in user:
            emails.append(user["email"])
    return emails
