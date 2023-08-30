#!/usr/bin/python3
"""
start, stop containers and pull images
"""
from models import storage
from models.container import Container
import requests
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/containers/start/<container_id>', strict_slashes=False, methods=['POST'])
def start_container(container_id):
    """
    api that starts container on server accepting app_name from user
    """
    base_url = "http://52.87.212.95:2375"
    start_url = f"{base_url}/containers/{container_id}/start"
    start_response = requests.post(start_url)
    if start_response.status_code == 204:
        api_url = f"{base_url}/containers/{container_id}/json"
        container_info = requests.get(api_url)
        if container_info.status_code == 200:
            container = container_info.json()
            return jsonify(container), 200
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/containers/stop/<container_id>/', strict_slashes=False, methods=['POST'])
def stop_container(container_id):
    """
    stops a specific container from running
    """
    base_url = "http://52.87.212.95:2375"
    stop_url = f"{base_url}/containers/{container_id}/stop"
    stop_response = requests.post(stop_url)
    if stop_response.status_code == 204:
        api_url = f"{base_url}/containers/{container_id}/json"
        container_info = requests.get(api_url)
        if container_info.status_code == 200:
            container = container_info.json()
            return jsonify(container), 200
        else:
            abort(404)
    else:
        abort(404)


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
    img_data = {}

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
                    user = storage.get(User, username=username).to_dict()
                    img_data['user_id'] = user['id']
                    img_data['status'] = 'stopped'
                    img_data['types'] = 'customized'
                    img_data['tag'] = image['RepoTags'][0].split(":")[1]
                    img_data['container_id'] = image['Id'].split(":")[1][:12]
                    img_data['name'] = image['RepoTags'][0].split(":")[0]
                    new_container = Container(**img_data)
                    storage.new(new_container)
                    storage.save()
                    return jsonify(new_container.to_dict()), 200

            abort(404, description=f"Image '{full_image_name}' not found.")
    else:
        abort(404, description=response.text)
