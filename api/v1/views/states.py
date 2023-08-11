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


# we could as well combine methods, e.g. methods=['GET','POST' etc...] and
# have an umbrella function with conditionals for each method,
# but it makes for easier debugging to seperate them.

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """ Retrieves list of all State objects:"""
    states_list = storage.all(State)
    # iterate through the list and append each item to a dictionary
    # and return as json
    return jsonify([s.to_dict() for s in states_list.values()])


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create State instance """
    bod_req = request.get_json() # create dictionary
    if bod_req is None:
        abort(400, "Not a JSON")
    if "name" not in bod_req:
        abort(400, "Missing name")
    # always remember to import "State" from models
    st_instance = State(**bod_req)
    storage.new(st_instance)
    storage.save()
    return make_response(jsonify(st_instance.to_dict()), 201)


# handling id's
def validate_instance():
    st_instance = storage.get("State", state_id)
    if not st_instance:
        abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state(state_id):
    """ Retrieve State instance """
    # st_instance = storage.get("State", state_id)
    # if not st_instance:
    #     abort(404)
    validate_instance()
    return jsonify(st_instance.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update State instance """
    # st_instance = storage.get("State", state_id)
    # if not st_instance:
    #     abort(404)
    validate_instance()

    bod_req = request.get_json()
    if bod_req is None:
        abort(400, "Not a JSON")

    for key, value in bod_req.items():
        # ignore 'created_at' and 'updated_at' key pairs
        if key != 'created_at' and k != 'updated_at' and key != 'id':
            setattr(st_instance, key, value)
    storage.save()
    return make_response(jsonify(st_instance.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete State instance """
    # st_instance = storage.get("State", state_id)
    # if not st_instance:
    #     abort(404)
    validate_instance()
    st_instance.delete()
    storage.save()
    return make_response(jsonify({}), 200)
