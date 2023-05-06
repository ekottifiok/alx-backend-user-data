#!/usr/bin/env python3
"""the session expiration auth module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Create a class SessionExpAuth that inherits from SessionAuth

    Args:
        SessionAuth (class): _description_
    """

    def __init__(self) -> None:
        """initializing the class module
        """
        super().__init__()
        duration = 0
        try:
            duration = int(getenv("SESSION_DURATION"))
        except TypeError:
            pass
        self.session_duration = duration

    def create_session(self, user_id=None):
        """creates a session from the user id

        Args:
            user_id (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """gets the userid for the session and ensures not expired

        Args:
            session_id (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if not session_id:
            return None
        session_id_data = self.user_id_by_session_id.get(session_id, None)
        if not session_id_data:
            return None
        user_id = session_id_data.get("user_id", None)
        created_at = session_id_data.get("created_at", None)
        if self.session_duration <= 0:
            return user_id
        if not created_at or \
                timedelta(seconds=self.session_duration)+created_at < datetime.now():
            return None
        return user_id
