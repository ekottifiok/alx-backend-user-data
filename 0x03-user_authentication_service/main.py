#!/usr/bin/env python3
"""test module all tests using assert
"""
from requests import delete, get, post, put

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://localhost:5001/"


def register_user(email: str, password: str):
    """attempts to register a user

    Args:
        email (str): _description_
        password (str): _description_
    """
    response = post(
        URL + "users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = post(
        URL + "users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str):
    """test what happens when the password is wrong and login

    Args:
        email (str): _description_
        password (str): _description_
    """
    response = post(
        URL + "sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401


def profile_unlogged():
    """checks what happens when you access the profile when not logged in
    """
    response = get(URL + "profile", cookies={"session_id": "nope"})
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """log in with correct parameters

    Args:
        email (str): _description_
        password (str): _description_

    Returns:
        str: _description_
    """
    response = post(
        URL + "sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies["session_id"]


def profile_logged(session_id: str):
    """test the profile logged in path

    Args:
        session_id (str): _description_
    """
    response = get(URL + "profile", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str):
    """test the logout handle

    Args:
        session_id (str): _description_
    """
    response = delete(URL + "sessions", cookies={"session_id": session_id})
    assert response.url == URL


def reset_password_token(email: str) -> str:
    """test the reset password tokens

    Args:
        email (str): _description_

    Returns:
        str: session_id
    """
    response = post(URL + "reset_password", data={"email": email + "fake"})
    assert response.status_code == 403
    response = post(URL + "reset_password", data={"email": email})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["email"] == email
    assert "reset_token" in response_json.keys()
    return response_json["reset_token"]


def update_password(email: str, reset_token: str, new_password: str):
    """test the update password endpoint

    Args:
        email (str): _description_
        reset_token (str): _description_
        new_password (str): _description_
    """
    response = put(
        URL + "/reset_password",
        data={
            "email": email,
            "reset_token": reset_token + "fake",
            "new_password": new_password
        }
    )
    assert response.status_code == 403
    response = put(
        URL + "/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
