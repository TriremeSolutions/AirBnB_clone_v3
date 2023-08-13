#!/usr/bin/python3
""" View for Place objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify
from flask import make_response, abort
from flask import request
import requests
import json
import models
from os import getenv
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_city_by_place(city_id):
    """
    Various actions obtainable on a city instance
    containing place instances
    """
    cy_instance = storage.get("City", city_id)
    if not cy_instance:
        abort(404)

    if request.method == 'GET':
        """ Retrieves the list of all Place instances """
        # iterate through the list and append each item to a dictionary
        # and return as json
        return jsonify([p.to_dict() for p in cy_instance.places])

    if request.method == 'POST':
        "Creates a new place instance in a City"
        bod_req = request.get_json()
        # If the HTTP body request is not a valid JSON,
        # raise a 400 error with the message Not a JSON
        if not bod_req:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key name,
        # raise a 400 error with the message Missing name
        if "user_id" not in bod_req:
            abort(400, 'Missing user_id')

        user_id = bod_req['user_id']
        if not storage.get("User", user_id):
            abort(404)
        if "name" not in bod_req:
            abort(400, 'Missing name')

        # create new place instance
        plc_instance = Place(**bod_req)
        # affix place instance to an existing city
        setattr(plc_instance, 'city_id', city_id)
        storage.new(plc_instance)
        # save
        storage.save()
        # Returns the new Place with the status code 201
        return make_response(jsonify(plc_instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_place_by_id(place_id):
    """
    Various actions obtainable on a place instance within
    a city instance with valid id
    """
    plc_instance = storage.get("Place", place_id)
    if not plc_instance:
        abort(404)

    if request.method == 'GET':
        """ Retrieve a Place in a City instance by its place_id """
        return jsonify(plc_instance.to_dict())

    if request.method == 'PUT':
        """ Update a Place instance """
        bod_req = request.get_json()
        if not bod_req:
            abort(400, "Not a JSON")

        for key, value in bod_req.items():
            ignore_keys = ['id', 'user_id',
                           'city_at', 'created_at', 'updated_at']
            if key not in ignore_keys:
                setattr(plc_instance, key, value)
        storage.save()
        return make_response(jsonify(cy_instance.to_dict()), 200)

    if request.method == 'DELETE':
        """ Delete Place instance """
        plc_instance.delete()
        storage.save()
        return make_response(jsonify({}), 200)
