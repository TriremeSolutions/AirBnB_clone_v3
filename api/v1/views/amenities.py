#!/usr/bin/python3
"""
View for Amenity objects that handles
all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify
from flask import make_response, abort
from flask import request
import models
from models import storage
from models.amenities import Amenity


# we could as well combine methods, e.g. methods=['GET','POST' etc...] and
# have an umbrella function with conditionals for each method,
# but it makes for easier debugging to seperate them.

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """ Retrieves list of all Amenity objects:"""
    amenities_list = storage.all(Amenity)
    # iterate through the list and append each item to a dictionary
    # and return as json
    return jsonify([s.to_dict() for s in amenities_list.values()])


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_Amenity():
    """ Create Amenity instance """
    bod_req = request.get_json()  # create dictionary
    if bod_req is None:
        abort(400, "Not a JSON")
    if "name" not in bod_req:
        abort(400, "Missing name")
    # always remember to import "Amenity" from models
    amn_instance = Amenity(**bod_req)
    storage.new(amn_instance)
    storage.save()
    return make_response(jsonify(amn_instance.to_dict()), 201)


# handling id's
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_Amenity(amenity_id):
    """ Retrieve Amenity instance """
    amn_instance = storage.get("Amenity", amenity_id)
    if not amn_instance:
        abort(404)
    return jsonify(amn_instance.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_Amenity(amenity_id):
    """ Update Amenity instance """
    amn_instance = storage.get("Amenity", amenity_id)
    if not amn_instance:
        abort(404)

    bod_req = request.get_json()
    if bod_req is None:
        abort(400, "Not a JSON")

    for key, value in bod_req.items():
        # ignore 'created_at' and 'updated_at' key pairs
        ignore_keys = ['created_at', 'updated_at', 'id']
        if key not in ignore_keys:
            setattr(amn_instance, key, value)
    storage.save()
    return make_response(jsonify(amn_instance.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_Amenity(amenity_id):
    """ Delete Amenity instance """
    amn_instance = storage.get("Amenity", amenity_id)
    if not amn_instance:
        abort(404)
    amn_instance.delete()
    storage.save()
    return make_response(jsonify({}), 200)
