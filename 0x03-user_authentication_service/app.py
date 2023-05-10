#!/usr/bin/env python3
"""Simple flask application that returns a simple message
"""
from flask import Flask, jsonify, request
from auth import Auth
from typing import Tuple

app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> Tuple[str, int]:
    """returns welcome in spanish

    Returns:
        Tuple[str, int]: json message and response code
    """
    return jsonify({"message": "Bienvenue"}), 200

@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> Tuple[str, int]:
    """registers a user

    Returns:
        Tuple[str, int]: json message and response code
    """
    try:
        json = request.get_json()
    except Exception as e:
        json = None
    email = json.get("email")
    if not email:
        return jsonify(message="email not found in json"), 400
    password = json.get("password")
    return jsonify(email=email, message="user created"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")