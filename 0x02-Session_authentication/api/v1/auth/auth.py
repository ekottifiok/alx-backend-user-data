#!/usr/bin/env python3
"""Auth Module that carries the Auth class and it functions
"""
from typing import List, TypeVar
from re import match
from flask import request as req


class Auth:
    """Auth model to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method def require_auth(self, path: str, excluded_paths:
        List[str]) -> bool:

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if path is None or excluded_paths is None:
            return True
        excluded_paths = [item if item[-1] != '/' else item[:-1]
                          for item in excluded_paths]
        path = path if path[-1] != '/' else path[:-1]
        for p in excluded_paths:
            if p[-1] == "*":
                regex = match(p, path)
                if regex and regex.group() == p[:-1]:
                    return False
            if p == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method def authorization_header(self, request=None) -> str:

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return None if request is None else req.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """that returns None - request will be the Flask request object
        """
        from flask import Flask
        request = Flask(__name__)
        return None

    def session_cookie(self, request=None):
        """creates session cookies

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """        
        return req.cookies.get("_my_session_id")
