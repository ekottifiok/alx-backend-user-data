#!/usr/bin/env python3
""" Implement a hash_password function that expects one
string argument name password and returns a salted, hashed
password, which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).

Use bcrypt to validate that the provided password matches
the hashed password.

"""
from bcrypt import checkpw, hashpw, gensalt


def hash_password(password: str) -> bytes:
    """Implement a hash_password function that expects
    one string argument name password and returns a salted,
    hashed password, which is a byte string.

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return hashpw(bytes(password, "utf-8"), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement an is_valid function that expects 2
    arguments and returns a boolean.

    Args:
        hashed_password (bytes): _description_
        password (str): _description_

    Returns:
        bool: True if the password matches and False if not
    """
    return checkpw(bytes(password, 'utf-8'), hashed_password)
