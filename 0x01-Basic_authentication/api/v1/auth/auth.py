#!/usr/bin/env python3
"""Auth Module that carries the Auth class and it functions
"""
from typing import List, TypeVar
from re import search


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
            if "*" in p:
                if search(p, path):
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
        if request is None or not isinstance(request, dict) or \
            'Authorization' not in request.keys():
            return None
        return request['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        return None
