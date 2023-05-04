#!/usr/bin/env python3
"""Module for Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request, sessions
from models.user import User


@app_views.route('/auth_session/login', methods=['GET'], strict_slashes=False)
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
        return jsonify({ "error": "no user found for this email" }), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.auth.session_auth import SessionAuth
    
    session = SessionAuth.create_session(user.get(id))
    return jsonify(user.to_json()).set_cookie("_my_session_id", session)
        
