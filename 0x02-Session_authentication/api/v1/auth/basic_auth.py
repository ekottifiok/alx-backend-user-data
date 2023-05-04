#!/usr/bin/env python3
"""Basic Authentication module
"""
from base64 import b64decode
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """_summary_
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """BasicAuth that returns the Base64 part of the Authorization
        header for a Basic Authentication:

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if authorization_header is None or \
            not isinstance(authorization_header, str) or \
                authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ that returns the decoded value of a Base64
        string base64_authorization_header:

        Args:
            base64_authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if not (base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            return None
        try:
            return b64decode(base64_authorization_header).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """in the class BasicAuth that returns the user email and
        password from theBase64 decoded value.

        Args:
            self (_type_): _description_
            str (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not (decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str)) or \
                ":" not in decoded_base64_authorization_header:
            return None, None
        splitted = decoded_base64_authorization_header.split(":")
        if len(splitted) < 2:
            return None, None
        return tuple([splitted[0], ":".join(splitted[1:])])

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> TypeVar('User'):  # type: ignore
        """ in the class BasicAuth that returns the User instance
        based on his email and password.

        Args:
            self (_type_): _description_
        """
        if not (user_email and isinstance(user_email, str)) or \
                not (user_pwd and isinstance(user_pwd, str)):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """
        try:
            self.user_object_from_credentials(
                *self.extract_user_credentials(
                    self.decode_base64_authorization_header(
                        self.extract_base64_authorization_header(
                            self.authorization_header(request)
                        )
                    )
                )
            )
        except Exception:
            return None
