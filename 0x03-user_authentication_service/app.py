#!/usr/bin/env python3
"""Simple flask application that returns a simple message
"""
from flask import abort, Flask, jsonify, redirect, request
from flask.wrappers import Response
from auth import Auth
from typing import Tuple
from werkzeug.wrappers.response import Response as Werk_Response

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> Tuple[Response, int]:
    """returns welcome in spanish

    Returns:
        Tuple[str, int]: json message and response code
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> Tuple[Response, int]:
    """registers a user

    Returns:
        Tuple[str, int]: json message and response code
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Tuple[Response, int]:
    """The request is expected to contain form data with
    "email" and a "password" fields.

    Returns:
        Tuple[str, int]: response
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    reply_json = jsonify({"email": email, "message": "logged in"})
    reply_json.set_cookie("session_id", str(AUTH.create_session(email)))
    return reply_json, 200


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Werk_Response:
    """you will implement a logout function to
    respond to the DELETE /sessions route.

    The request is expected to contain the session
    ID as a cookie with key "session_id".

    Returns:
        Tuple[Response, int]: _description_
    """
    user = AUTH.get_user_from_session_id(
        str(request.cookies.get("session_id"))
    )
    if not user:
        abort(403)
    AUTH.destroy_session(str(user.id))
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Tuple[Response, int]:
    """_summary_

    Returns:
        Tuple[Response, int]: _description_
    """
    user = AUTH.get_user_from_session_id(
        str(request.cookies.get("session_id"))
    )
    if not user:
        abort(403)
    return jsonify({"email": str(user.email)}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Tuple[Response, int]:
    """_summary_

    Returns:
        Tuple[Response, int]: _description_
    """
    email = request.form.get("email")
    if not email:
        abort(403)
    return jsonify(
        email=email,
        reset_token=AUTH.get_reset_password_token(email)
    ), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> Tuple[Response, int]:
    """The request is expected to contain form data with fields
    "email", "reset_token" and "new_password".

    Update the password. If the token is invalid, catch the exception
    and respond with a 403 HTTP code.

    Returns:
        Tuple[Response, int]: _description_
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not all([email, reset_token, new_password]):
        abort(403)
    try:
        AUTH.update_password(str(reset_token), str(new_password))
    except ValueError:
        abort(403)
    return (
        jsonify({"email": email, "message": "Password updated"}),
        200
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
