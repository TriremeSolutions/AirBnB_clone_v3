#!/usr/bin/python3
"""this is the views index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


# create route
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a json file"""
    return jsonify(status="OK")
