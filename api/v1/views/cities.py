#!/usr/bin/python3
"""
View for State objects that handles
all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify
from flask import make_response, abort
from flask import request
import models
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """ Retrieves the list of all City instances of a State """
    st_instance = storage.get("State", state_id)
    if not st_instance:
        abort(404)
    # iterate through the list and append each item to a dictionary
    # and return as json
    return jsonify([c.to_dict() for c in st_instance.cities])


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    "Creates a new city instance in a State"
    st_instance = storage.get("State", state_id)
    if not st_instance:
        abort(404, 'Not found')
    bod_req = request.get_json()
    # If the HTTP body request is not a valid JSON,
    # raise a 400 error with the message Not a JSON
    if not bod_req:
        abort(400, 'Not a JSON')
    # If the dictionary doesn’t contain the key name,
    # raise a 400 error with the message Missing name
    if "name" not in bod_req:
        abort(400, 'Missing name')
    # create new city instance
    cy_instance = City(**bod_req)
    # affix city instance to an existing state
    setattr(city, 'state_id', state_id)
    storage.new(cy_instance)
    # save
    storage.save()
    # Returns the new City with the status code 201
    return make_response(jsonify(cy_instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_city_by_id(city_id):
    """
    Various actions obtainable on a city instance with valid id
    """
    cy_instance = storage.get("City", city_id)
    # If city_id not linked to any City instance, raise 404 error
    if not cy_instance:
        abort(404)

    if request.method == 'GET':
        """ Retrieve a City in a State instance by its city_id """
        return jsonify(cy_instance.to_dict())

    if request.method == 'DELETE':
        """ Delete City instance """
        cy_instance.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        """ Update a City instance """
        bod_req = request.get_json()
        if not bod_req:
            abort(400, "Not a JSON")

        for key, value in bod_req.items():
            ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
            if key not in ignore_keys:
                setattr(cy_instance, key, value)
        storage.save()
        return make_response(jsonify(cy_instance.to_dict()), 200)
