#!/usr/bin/python3
"""
create route for our app_views blue print
"""
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    return {"status": "OK"}
