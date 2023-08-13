#!/usr/bin/python3
"""
View for User objects that handles
all default RESTFul API actions:
"""
from api.v1.views import app_views
from flask import jsonify
from flask import make_response, abort
from flask import request
import models
from models import storage
from models.user import User


# we could as well combine methods, e.g. methods=['GET','POST' etc...] and
# have an umbrella function with conditionals for each method,
# but it makes for easier debugging to seperate them.

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """ Retrieves list of all User objects:"""
    users_list = storage.all(User)
    # iterate through the list and append each item to a dictionary
    # and return as json
    return jsonify([s.to_dict() for s in users_list.values()])


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_User():
    """ Create User instance """
    bod_req = request.get_json()  # create dictionary
    if bod_req is None:
        abort(400, "Not a JSON")
    if "email" not in bod_req:
        abort(400, 'Missing email')
    if "password" not in bod_req:
        abort(400, 'Missing password')

    # always remember to import "User" from models
    usr_instance = User(**bod_req)
    storage.new(usr_instance)
    storage.save()
    return make_response(jsonify(usr_instance.to_dict()), 201)


# handling id's
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_User(user_id):
    """ Retrieve User instance """
    usr_instance = storage.get("User", user_id)
    if not usr_instance:
        abort(404)
    return jsonify(usr_instance.to_dict())


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_User(user_id):
    """ Update User instance """
    usr_instance = storage.get("User", user_id)
    if not usr_instance:
        abort(404)

    bod_req = request.get_json()
    if bod_req is None:
        abort(400, "Not a JSON")

    for key, value in bod_req.items():
        # ignore 'created_at' and 'updated_at' key pairs
        ignore_keys = ['created_at', 'updated_at', 'id']
        if key not in ignore_keys:
            setattr(usr_instance, key, value)
    storage.save()
    return make_response(jsonify(usr_instance.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_User(user_id):
    """ Delete User instance """
    usr_instance = storage.get("User", user_id)
    if not usr_instance:
        abort(404)
    usr_instance.delete()
    storage.save()
    return make_response(jsonify({}), 200)
