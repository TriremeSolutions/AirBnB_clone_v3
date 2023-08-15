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
        return make_response(jsonify(plc_instance.to_dict()), 200)

    if request.method == 'DELETE':
        """ Delete Place instance """
        plc_instance.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
# def places_search():
#     """
#     Retrieves all Place objects using JSON in request body
#     """
#     # If the HTTP request body is not valid JSON,
#     # raise a 400 error with the message Not a JSON

#     bod_req = request.get_json()
#     if bod_req is None:
#         abort(400, "Not a JSON")

#     # If the JSON body is empty, or each list of all keys are empty:
#     # retrieve all Place objects
#     st = bod_req['states']
#     cy = bod_req['cities']
#     amn = bod_req.get('amenities')
#     # recall that these are lists of ids, not actual names

#     if not bod_req or (not st and not cy and not amn):
#         plc_list = storage.all(Place)
#         return jsonify([p.to_dict() for p in plc_list.values()])

#     # implicit else, return empty json.
#     plc_list = []
#     # also a proactive else for future if-conditions, as well

#     # If states list is not empty, results should include all Place objects
#     # for each State id listed

#     if st and len(st) > 0:
#         st_list = [storage.get("State", n) for n in st]
#         # json file of state names, including their ids

#         # iterate for every state in the states
#         for x in st_list:
#             # of every city in that state
#             for y in x.cities:
#                 # for every place in that city
#                 [plc_list.append(z) for z in y.places]
#                 # add to the list of places and return as json,
#                 # after all other if-blocks

#     if cy and len(cy) > 0:
#         cy_list = [storage.get("City", n) for n in cy]
#         for x in cy_list:
#             [plc_list.append(y) for y in x.places if y not in plc_list]

#     if not plc_list:
#         plc_list = [n for n in storage.all(Place).values()]

#     # If amenities list is not empty, limit search results
#     # to only Place objects having all Amenity ids listed

#     if amn:
#         # create list of valid amenity instances
#         amn_list = [storage.get("Amenity", n) for n in amn]
#         count = 0
#         limit = len(plc_list)
#         HBNB_API_HOST = getenv('HBNB_API_HOST')
#         HBNB_API_PORT = getenv('HBNB_API_PORT')

#         port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
#         url = "http://0.0.0.0:{}/api/v1/places/".format(port)
#         while count < limit:
#             place = plc_list[count]
#             url = url + '{}/amenities'
#             req = url.format(place.id)
#             res = requests.get(req)
#             jlod = json.loads(res.text)
#             amen = [storage.get("Amenity", x['id']) for x in jlod]
#             for a in amn_list:
#                 if a not in amen:
#                     plc_list.pop(count)
#                     count -= 1
#                     limit -= 1
#                     break
#             count += 1
#     # the proactive else
#     return jsonify([p.to_dict() for p in plc_list])

def places_search():
    """
        Retrieves all Place objects using JSON in request body
    """
    plc_list = [p for p in storage.all('Place').values()]
    bod_req = request.get_json()
    if bod_req is None:
        abort(400, 'Not a JSON')
    st = bod_req.get('states')

    if st and len(st) > 0:
        cy_list = storage.all('City')
        st_match_cy = set([city.id for city in cy_list.values()
                            if city.state_id in st])
    else:
        st_match_cy = set()
    
    cy = bod_req.get('cy')
    
    if cy and len(cy) > 0:
        cy = set([
            c_id for c_id in cy if storage.get('City', c_id)])
        st_match_cy = st_match_cy.union(cy)
    
    amenities = bod_req.get('amenities')
    
    if len(st_match_cy) > 0:
        plc_list = [p for p in plc_list if p.city_id in st_match_cy]
        
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in plc_list]
        return jsonify(result)
    
    places_amenities = []
    
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in plc_list:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = plc_list
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
