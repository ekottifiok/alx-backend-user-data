#!/usr/bin/env python3
"""Authorization Module
"""
from db import DB
from user import User
from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """In this task you will define a _hash_password method that
    takes in a password string arguments and returns bytes.

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    return hashpw(password.encode("utf8"), gensalt())


def _generate_uuid() -> str:
    """The function should return a string representation
    of a new UUID. Use the uuid module.

    Returns:
        str: uuid4
    """
    from uuid import uuid4
    return str(uuid4())


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
        self._db.add_user(email, _hash_password(password).decode())
        return self._db.find_user_by(email=email)

    def valid_login(self, email: str, password: str) -> bool:
        """It should expect email and password
        required arguments and return a boolean.

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            bool: true if valid and false if not
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        if email == user.email and checkpw(password.encode(), bytes(
                str(user.hashed_password), encoding="utf-8")):
            return True
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """It takes an email string argument and returns the
        session ID as a string.

        The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the
        user's session_id, then return the session ID.

        Args:
            email (str): email of the user

        Returns:
            str: session id
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = session_id
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """It takes a single session_id string argument and
        returns the corresponding User or None.

        Args:
            session_id (str): _description_

        Returns:
            User: _description_
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """The method takes a single user_id integer argument and
        returns None.

        The method updates the corresponding useR's session ID to None.

        Args:
            user_id (str): _description_
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """It take an email string argument and returns a string.
        Find the user corresponding to the email. If the user does not exist,
        raise a ValueError exception. If it exists, generate a UUID and update
        the user's reset_token database field. Return the token.

        Args:
            email (str): _description_

        Returns:
            str: _description_
        """
        reset_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user.reset_token = reset_token
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): _description_
            password (str): _description_
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        user.hashed_password = _hash_password(password).decode()
        user.reset_token = None
