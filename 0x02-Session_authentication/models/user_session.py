#!/usr/bin/env python3
"""User Session module
"""
from models.base import Base


class UserSession(Base):
    """UserSession Class

    Args:
        Base (_type_): _description_
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a User Session instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
