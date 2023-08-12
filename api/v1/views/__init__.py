#!/usr/bin/python3
"""views init file from which app_views is imported"""
from flask import Blueprint

# create Blueprint instance with url prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# wildcard import of contents from package api.v1.views
# ignore pycodestyle warning
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
