from datetime import datetime

passwords = [
    "Fluffy",
    "Galactic",
    "Mangoes",
    "Subatomic",
    [
        "Monkey",
        "Bot",
        "Dance",
        "Party",
        "Speed",
        "Racer",
        "Guitar",
        "Goat",
        "Camera",
        "Piano",
        "Throne",
        "Jellyfish",
    ],
]


def get_password(level):
    if level == len(passwords) - 1:
        hour = datetime.now().hour
        # We utilise the hour of the day to choose the idx of the password
        key = hour % len(passwords[level])
        return passwords[-1][key]
    if level < len(passwords):
        return passwords[level]
    return None
