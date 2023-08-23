#!/usr/bin/python3
"""
setting up blueprint modules
"""
from flask import Blueprint

app_views = Blueprint("appviews", __name__)

from api.v1.views.index import *
