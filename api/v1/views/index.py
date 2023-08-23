#!/usr/bin/python3
"""
create route for our app_views blue print
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from models.container import Container


@app_views.route("/status", strict_slashes=False)
def status():
    return {"status": "OK"}


@app_views.route("/stats", strict_slashes=False)
def stats():
    return {
        "users": storage.count(User),
        "container": storage.count(Container)
    }
