#!/usr/bin/python3
"""Script runs flask, imports blueprint"""
from flask import Flask
from flask import jsonify
from flask import make_response
from flask_cors import CORS
import models
from models import storage
from os import getenv
from api.v1.views import app_views

# app, instance of flask
app = Flask(__name__)

# register blueprint to app instance
app.register_blueprint(app_views)

# Update api/v1/app.py to create a CORS
# instance allowing: /* for 0.0.0.0
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# declare a method to handle
# @app.teardown_appcontext that calls storage.close()


@app.teardown_appcontext
def teardown_session(exception):
    """Ends session for stroage"""
    storage.close()


# create 404 handler; returns JSON-formatted response.
@app.errorhandler(404)
def not_found(error):
    """Retrun JSON response"""
    return make_response(
                         jsonify(
                            {"error": "Not found"}
                         ), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
