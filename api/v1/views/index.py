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


# Create an endpoint that retrieves the number of each objects by type:
@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    "Retrieve number of each type of object/instance"
    return jsonify(users=storage.count("User"),
                   states=storage.count("State"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   amenities=storage.count("Amenity"),
                   reviews=storage.count("Review"))
