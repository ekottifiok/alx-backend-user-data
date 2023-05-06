#!/usr/bin/env python3
"""Session Authentication module
"""
from api.v1.auth.auth import Auth
from uuid import UUID, uuid4
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class is the main class for the session

    Args:
        Auth (_type_): _description_
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """that creates a Session ID for a user_id

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: session_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """that returns a User ID based on a Session ID

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a user instance based on a cookie value

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request))
        )

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session from the request.

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """        """
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
