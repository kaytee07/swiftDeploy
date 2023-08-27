#!/usr/bin/python3
"""
start, stop containers and pull images
"""
from models import storage
from models.container import Container
from models.user import User
from app.v1.views import app_view
from flask import abort, request, jsonify

@app_view.route('/container/<username>/start/', strict_slashes=False, methods=['POST'])
def start_container(username):
    pass


@app_view.route('/container/<username>/stop/<container_id>', strict_slashes=False, methods=['POST'])
def stop_container(username):
    pass
