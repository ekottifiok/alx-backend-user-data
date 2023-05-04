#!/usr/bin/env python3
""" Module of Index views
"""
from flask import abort, jsonify
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def test_unauthorized() -> str:
    """tests unauthorized 

    Returns:
        str: _description_
    """
    abort(401)


@app_views.route(
    '/api/v1/forbidden',
    methods=['GET'],
    strict_slashes=False
)
def tes_forbidden() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    abort(403)


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
