#!/usr/bin/python3
"""
start, stop containers and pull images
"""
from models import storage
from models.container import Container
from paramiko import SSHException
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify
from fabric import Connection


def login_to_docker(c, dockerID, password):
    try:
        result = c.run(f"./logintodockerhub {dockerID} {password}")
        return result.stdout
    except SSHException as e:
        return {"error": "SSH connection error: " + str(e)}, 500
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500

@app_views.route('/containers/<username>/hublogin', strict_slashes=False, methods=['POST'])
def login_dockerHub(username):
    """
    login into user's docker hub account with their docker from requests
    and password they'll enter
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    user = storage.get(User, username=username).to_dict()
    if user:
        conn = Connection(host="ubuntu@52.87.212.95")
        result = login_to_docker(conn, user['dockerID'], data['password'])

        return jsonify({
            "dockerID": user['dockerID'],
            "hubpass": data["password"],
            "message": result
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
