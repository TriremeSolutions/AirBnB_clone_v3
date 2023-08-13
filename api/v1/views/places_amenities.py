#!/usr/bin/python3
"""
View for the link between Place objects
and Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify
from flask import make_response, abort
from flask import request
import models
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def list_place_amenities(place_id):
    """
    Retrieves the list of all Amenities instances
    in a Place instance with valid id
    """
    plc_instance = storage.get("Place", place_id)
    if not plc_instance:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        ams = [s.to_dict() for s in plc_instance.amenities]
    else:
        ams = [storage.get("Amenity", id).to_dict()
               for id in plc_instance.amenity_ids]
    return jsonify(ams)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST', 'DELETE'],
                 strict_slashes=False)
def handle_places_and_amenity(place_id, amenity_id):
    """
    Various actions obtainable on an amenity instance
    and its place instance with valid id
    """
    plc_instance = storage.get("Place", place_id)
    if not plc_instance:
        abort(404)

    amn_instance = storage.get("Amenity", amenity_id)
    if not amn_instance:
        abort(404)

    def check(x, y):
        if x not in y:
            abort(404)

    if request.method == 'POST':
        # link an amenity instance to a place instance
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amn_instance in plc_instance.amenities:
                return make_response(jsonify(amn_instance.to_dict()), 200)
            plc_instance.amenities.append(amn_instance)
        else:
            # i.e. filestorage
            if amenity_id in plc_instance.amenity_ids:
                return make_response(jsonify(amn_instance.to_dict()), 200)
            plc_instance.amenity_ids.append(amenity_id)

        storage.save()
        return make_response(jsonify(amn_instance.to_dict()), 201)

    if request.method == 'DELETE':
        """ delete an amenity from a place """
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            check(amn_instance, plc_instance.amenities)
        else:
            # i.e. filestorage
            check(amenity_id, plc_instance.amenity_ids)
            position = plc_instance.amenity_ids.index(amenity_id)
            plc_instance.amenity_ids.pop(position)

        amn_instance.delete()
        storage.save()
        return make_response(jsonify({}), 200)
