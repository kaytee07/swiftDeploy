#!/usr/bin/python3
"""
create route for our app_views blue print
"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    return {"status": "OK"}
