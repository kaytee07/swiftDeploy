#!/usr/bin/python3
"""
start, stop containers and pull images
"""
from models import storage
from models.container import Container
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify
from fabric import Connection


@app_views.route('/containers/<username>/hublogin', strict_slashes=False, methods=['POST'])
def login_dockerHub(username):
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    user = storage.get(User, username=username).to_dict()
    if user:
        c = Connection(host="ubuntu@52.87.212.95")
        result = c.run("ls projects")

        return jsonify({
            "dockerID": user['dockerID'],
            "hubpass": data["password"],
            "message": result.stdout
        }), 200


@app_views.route('/containers/<username>/hublogout', strict_slashes=False, methods=['POST'])
def logout_dockerHub():
    return jsonify({"status": "loggedout"})


@app_views.route('/containers/<username>/start/', strict_slashes=False, methods=['POST'])
def start_container(username):
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'password' not in data:
        abort(400, description="Missing password")

    user = storage.get(User, username=username).to_dict()
    if user:
        return jsonify({
            'name': data['name'],
            'dockerID': data['dockerID'],
            'status': 'start container',
            'first_name': user['first_name']
        }), 200
    else:
        abort(404)


@app_views.route('/containers/<username>/stop/<container_id>', strict_slashes=False, methods=['POST'])
def stop_container(username):
    return jsonify({'status': 'stop container'}), 200
