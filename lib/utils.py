from datetime import datetime

from fastapi import HTTPException

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


def get_password(level: int):
    """
    Returns the password for the given level - note that level goes from 1 to 5 in this case.
    """
    if level < 1 or level > len(passwords):
        raise HTTPException(status_code=400, detail=f"Invalid level of {level}")

    if level == len(passwords):
        hour = datetime.now().hour
        # We utilise the hour of the day to choose the idx of the password
        key = hour % len(passwords[-1])
        return passwords[-1][key]

    return passwords[level - 1]
