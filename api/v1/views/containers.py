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


def login_to_docker(dockerID, password):
    """
    login to dockerhub from assigned server
    @dockerID: dockerhub dockerID
    @password: dockerhub password
    """
    try:
        conn = Connection(host="ubuntu@52.87.212.95")
        result = conn.run(f"./logintodockerhub {dockerID} {password}")
        return result.stdout
    except SSHException as e:
        return {"error": "SSH connection error: " + str(e)}, 500
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


def logout_from_docker():
    """
    logout from dockerhub on assigned server
    """
    try:
        conn = Connection(host="ubuntu@52.87.212.95")
        result = conn.run("./logoutdockerhub")
        return result.stdout
    except SSHException as e:
        return {"error": "SSH connection error: " + str(e)}, 500
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


def start_docker_container(dockerID, app_name):
    """
    start docker container from image on docker hub
    @dockerID: user's dockerID
    @app_name: user's app name on docker hub
    """
    try:
        conn = Connection(host="ubuntu@52.87.212.95")
        result = conn.run(f"./startdockercontainer {dockerID} {app_name}")
        return result.stdout
    except SSHException as e:
        return {"error": "SSH connection error: " + str(e)}, 500
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


def stop_docker_container(containerID):
    """
    stop docker container
    @containerID: user's dockerID
    """
    try:
        conn = Connection(host="ubuntu@52.87.212.95")
        result = conn.run(f"./stopdockercontainer {containerID}")
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
        result = login_to_docker(user['dockerID'], data['password'])
        return jsonify({
            "dockerID": user['dockerID'],
            "hubpass": data["password"],
            "message": result
        }), 200
    else:
        abort(404, description="user cannot be found")


@app_views.route('/containers/hublogout', strict_slashes=False, methods=['POST'])
def logout_dockerHub():
    result = logout_from_docker()
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

    result = start_docker_container(user['dockerID'], data['app_name'])
    if user:
        return jsonify({"user": result}), 200
    else:
        abort(404, 'user not found')


@app_views.route('/containers/stop/<container_id>/', strict_slashes=False, methods=['POST'])
def stop_container(container_id):
    """
    stops a specific container from running
    """
    result = stop_docker_container(container_id)
    return jsonify({'status': result}), 200


@app_views.route('/containers', strict_slashes=False)
def get_containers():
    """
    get pre defined containers and those imported by you
    """
    api_url = 'http://52.87.212.95:2375/images/json'
    response = requests.get(api_url)

    if response.status_code == 200:
        results = response.json()
        return jsonify(results), 200
    else:
        return jsonify({"error": "Failed to fetch containers"}), 500


@app_views.route('/container/pull')
def pull_containers():
    """
    pull container from dockerhub
    """
    data = request.get_json()
    api_url = f"http://localhost:2375/images/create?fromImage={data['name']}&tag={data['tag']}"

    response = requests.post(api_url)

    if response.status_code == 200:
        print(f"Image {data['name']}:{data['tag']} pulled successfully.")
        return jsonify(response), 200
    else:
        print(f"Failed to pull image {data['name']}:{data['tag']}.")
        abort(404, description=response.text)
