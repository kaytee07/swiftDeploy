#!/usr/bin/python3
"""
setting up blueprint modules
"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint("appviews", __name__)
