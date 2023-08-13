#!/usr/bin/python3
""" View for Review objects that handles default API actions """

from api.v1.views import app_views
from flask import jsonify
from flask import make_response, abort
from flask import request
import models
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_place_by_reviews(place_id):
    """
    Various actions obtainable on a city instance
    containing place instances
    """
    plc_instance = storage.get("Place", place_id)
    if not plc_instance:
        abort(404)

    if request.method == 'GET':
        return jsonify([p.to_dict() for p in plc_instance.reviews])

    if request.method == 'POST':
        "Creates a new review instance for a Place"
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
        if "text" not in bod_req:
            abort(400, 'Missing text')

        # create new review instance
        rev_instance = Review(**bod_req)
        # affix review instance to an existing place
        setattr(rev_instance, 'place_id', place_id)
        storage.new(rev_instance)
        # save
        storage.save()
        # Returns the new Place with the status code 201
        return make_response(jsonify(rev_instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_review_by_id(review_id):
    """
    Various actions obtainable on a review instance within
    a place instance with valid id
    """
    rev_instance = storage.get("Review", review_id)
    if not rev_instance:
        abort(404)

    if request.method == 'GET':
        """ Retrieve a Review for a Place instance by its review_id """
        return jsonify(rev_instance.to_dict())

    if request.method == 'PUT':
        """ Update a Review instance """
        bod_req = request.get_json()
        if not bod_req:
            abort(400, "Not a JSON")

        for key, value in bod_req.items():
            ignore_keys = ['id', 'user_id',
                           'place_id', 'created_at', 'updated_at']
            if key not in ignore_keys:
                setattr(rev_instance, key, value)
        storage.save()
        return make_response(jsonify(rev_instance.to_dict()), 200)

    if request.method == 'DELETE':
        """ Delete Place instance """
        rev_instance.delete()
        storage.save()
        return make_response(jsonify({}), 200)
