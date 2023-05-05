#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import abort, Flask, jsonify, request
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def run_before_request():
    """run this command before any request is made
    in this I"m checking if the authorization is set
    """
    e = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/"
    ]
    if auth is None \
            or not auth.require_auth(request.path, e):
        return
    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)
    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)
    request.current_user = current_user


@app.errorhandler(401)
def unauthorized_access(_) -> str:
    """error handler for unauthorized access

    Args:
        error (_type_): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(_) -> str:
    """error handler for 403 status code

    Args:
        error (any): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(_) -> str:
    """Not found handler returns

    Args:
        error (_type_): _description_

    Returns:
        str: json
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
