#!/usr/bin/env python3
"""Database module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """Database class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()

        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a user to the database and returns the id

        Args:
            email (str): _description_
            hashed_password (str): _description_

        Returns:
            int: the class id
        """
        try:
            user_instance = User(
                email=email,
                hashed_password=hashed_password
            )
            self._session.add(user_instance)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user_instance = None
        return user_instance

    def find_user_by(self, **kwargs) -> User:
        """This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by the method's
        input arguments. No validation of input arguments
        required at this point.

        Raises:
            InvalidRequestError: _description_
            NoResultFound: _description_

        Returns:
            User: _description_
        """
        keys, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                keys.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*keys).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """method that takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.

        Args:
            user_id (int): _description_

        Returns:
            _type_: _description_
        """
        if len(kwargs) == 0:
            user = self.find_user_by(id=user_id)
            if user is None:
                return
            for key, value in kwargs.items():
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError()
            self._session.commit()
