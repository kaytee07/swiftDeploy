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
    try:
        get_cont = storage.get(Container, container_id=container_id).to_dict()
        print(get_cont)

        remote_docker_host = 'http://52.87.212.95:2375'
        headers = {'Content-Type': 'application/json'}

        create_url = f"{remote_docker_host}/containers/create"
        create_data = {
            "Image": f"{get_cont['name']}:{get_cont['tag']}",
            "Detach": True
        }

        response = requests.post(create_url, json=create_data, headers=headers)
        container_id = response.json()
        print(container_id)

        return jsonify({response.json}), 200
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        abort(500)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        abort(500)


@app_views.route('/containers/stop/<container_id>/', strict_slashes=False, methods=['POST'])
def stop_container(container_id):
    """
    stops a specific container from running
    """
    try:
        get_cont = storage.get(Container, container_id=container_id).to_dict()
        print(get_cont)
        stop_url = f"http://52.87.212.95:2375/containers/{container_id}/start"
        stop_response = requests.post(stop_url)

        if stop_response.status_code == 204:
            print('did it hit')

            api_url = f"http://52.87.212.95:2375/containers/{container_id}/json"
            container_info = requests.get(api_url)

            if container_info.status_code == 200:
                print('yes it hit')
                container = container_info.json()
                return jsonify(container), 200
            else:
                abort(404)
        else:
            abort(404)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        abort(500)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        abort(500)


@app_views.route('/containers/<username>', strict_slashes=False)
def get_containers(username):
    """
    get pre defined containers and those imported by you
    """
    containers = {}
    users = storage.get(User, username=username).to_dict()
    get_cont = storage.all(Container)
    for key, value in get_cont.items():
        print(value.to_dict()['types'])
        if value.to_dict()['types'] is None or  value.to_dict()['user_id'] == users['id']:
            containers[value.to_dict()['name']] = value.to_dict()
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
