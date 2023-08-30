#!/usr/bin/python3
"""
start, stop containers and pull images
"""
from models import storage
from models.container import Container
from paramiko import SSHException
import requests
import json
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify
from fabric import Connection



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
        return jsonify({
            "dockerID": user['dockerID'],
            "hubpass": data["password"],
            "message": result
        }), 200
    else:
        abort(404, description="user cannot be found")


@app_views.route('/containers/hublogout', strict_slashes=False, methods=['POST'])
def logout_dockerHub():
    return jsonify({"status": result})


@app_views.route('/containers/<username>/start/', strict_slashes=False, methods=['POST'])
def start_container(username):
    """
    api that starts container on server accepting app_name from user
    """
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'app_name' not in data:
        abort(400, description="Missing app name")

    user = storage.get(User, username=username).to_dict()
    if user:
        return jsonify({"user": result}), 200
    else:
        abort(404, 'user not found')


@app_views.route('/containers/stop/<container_id>/', strict_slashes=False, methods=['POST'])
def stop_container(container_id):
    """
    stops a specific container from running
    """
    return jsonify({'status': result}), 200


@app_views.route('/containers', strict_slashes=False)
def get_containers():
    """
    get pre defined containers and those imported by you
    """
    containers = {}
    get_cont = storage.all(Container)
    for key, value in get_cont.items():
        containers[value.to_dict()['name']] = value.to_dict()
    print(containers)
    return jsonify(containers), 200


@app_views.route('/containers/<username>/pull', strict_slashes=False, methods=['POST'])
def pull_containers(username):
    """
    pull container from Docker Hub
    """
    data = request.get_json()

    if 'docker_id' in data and data['docker_id']:
        full_image_name = f"{data['docker_id']}/{data['name']}:{data['tag']}"
    else:
        full_image_name = f"{data['name']}:{data['tag']}"

    api_url = f'http://52.87.212.95:2375/images/create?fromImage={full_image_name}'
    response = requests.post(api_url)

    if response.status_code == 200:
        api_url = 'http://52.87.212.95:2375/images/json'
        response = requests.get(api_url)

        if response.status_code == 200:
            images = response.json()

            for image in images:
                if full_image_name in image.get('RepoTags', []):
                    return jsonify({full_image_name: data['tag']}), 200

            abort(404, description=f"Image '{full_image_name}' not found.")
    else:
        abort(404, description=response.text)

