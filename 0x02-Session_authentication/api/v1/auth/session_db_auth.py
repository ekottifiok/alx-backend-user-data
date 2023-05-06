#!/usr/bin/env python3
"""Session DB Auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth Class

    Args:
        SessionExpAuth (class): _description_
    """

    def create_session(self, user_id=None):
        """Overload def create_session(self, user_id=None): that creates
        and stores new instance of UserSession and returns the Session ID

        Args:
            user_id (_type_, optional): _description_. Defaults to None.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = session_id
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload def user_id_for_session_id(self, session_id=None):
        that returns the User ID by requesting UserSession in the database
        based on session_id

        Args:
            session_id (_type_, optional): _description_. Defaults to None.
        """
        if not session_id:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if not user_id:
            user_session = UserSession()
            user_session.load_from_file()
            user_session = user_session.search({"session_id": session_id})[0]
            if not user_session or timedelta(
                seconds=self.session_duration
            ) + user_session.created_at < datetime.now():
                return None

            user_id = user_session.user_id
            if not user_id:
                return None
        return user_id

    def destroy_session(self, request=None):
        """Overload def destroy_session(self, request=None): that destroys
        the UserSession based on the Session ID from the request cookie

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        user_session = UserSession.get(
            self.user_id_for_session_id(
                self.session_cookie(request)
            )
        )
        if not user_session:
            return None
        user_session.remove()
        super().destroy_session(request)
