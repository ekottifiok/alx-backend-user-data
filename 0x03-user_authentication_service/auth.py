#!/usr/bin/env python3
"""Authorization Module
"""
from db import DB
from user import User
from bcrypt import gensalt, hashpw
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """In this task you will define a _hash_password method that
    takes in a password string arguments and returns bytes.

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return hashpw(str.encode(password), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """should take mandatory email and password string
        arguments and return a User object.

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            User: _description_
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError
        except Exception as e:
            if e.__class__.__name__ == "ValueError":
                print("User {} already exists".format(email))
                raise ValueError
        hashed_pwd = _hash_password(password)
        self._db.add_user(email, hashed_pwd)
        return self._db.find_user_by(email=email)
