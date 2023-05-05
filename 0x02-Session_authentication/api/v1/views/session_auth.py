#!/usr/bin/env python3
"""Module for Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """GET for /auth_session/login

    Returns:
        str: _description_
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': email})
        if user == []:
            raise Exception
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    from os import getenv

    sessiond_id = auth.create_session(getattr(user, 'id'))
    ret = jsonify(user.to_json())
    ret.set_cookie(
        getenv("SESSION_NAME"), sessiond_id
    )
    return ret


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout() -> str:
    """deletes a session and if deleted 

    Returns:
        str: an empty json
    """
    from api.v1.app import auth
    from flask import abort

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
