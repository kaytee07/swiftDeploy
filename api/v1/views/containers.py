#!/usr/bin/python3
"""
start, stop containers and pull images
"""
from models import storage
from models.container import Container
import requests
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify, session, redirect, url_for


@app_views.route('/containers/start/<image_id>', strict_slashes=False, methods=['POST'])
def start_container(image_id):
    """
    api that starts container on server accepting app_name from user
    """
    try:
        get_cont = storage.get(Container, image_id=image_id)
        print(get_cont)
        get_cont_dict = get_cont.to_dict()

        remote_docker_host = 'http://52.87.212.95:2375'
        headers = {'Content-Type': 'application/json'}

        create_url = f"{remote_docker_host}/containers/create"
        create_data = {
            "Image": f"{get_cont_dict['name']}:{get_cont_dict['tag']}",
            "Detach": True
        }

        response = requests.post(create_url, json=create_data, headers=headers)
        container_id = response.json()['Id']
        print(container_id)
        start_url = f"http://52.87.212.95:2375/containers/{container_id}/start"
        start_container = requests.post(start_url)
        if start_container.status_code == 204:
            api_url = f"http://52.87.212.95:2375/containers/{container_id}/json"
            container_info = requests.get(api_url)
            if container_info.status_code == 200:
                container = container_info.json()
                print(container)
                info = container['State']['Status']
                if info == 'running':
                    get_cont.status = info
                    get_cont.container_id = container_id
                    get_cont.port = 3000
                    storage.new(get_cont)
                    storage.save()
                return jsonify(get_cont.to_dict()), 200
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        abort(404)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        abort(404)


@app_views.route('/containers/stop/<image_id>', strict_slashes=False, methods=['POST'])
def stop_container(image_id):
    """
    stops a specific container from running
    """
    try:
        get_cont = storage.get(Container, image_id=image_id)
        if get_cont:
            container_id = get_cont.to_dict()['container_id']
        else:
            abort(404)
        stop_url = f"http://52.87.212.95:2375/containers/{container_id}/stop"
        stop_response = requests.post(stop_url)
        if stop_response.status_code == 204:
            print('did it hit')
            api_url = f"http://52.87.212.95:2375/containers/{container_id}/json"
            container_info = requests.get(api_url)
            if container_info.status_code == 200:
                container = container_info.json()
                info = container['State']['Status']
                if info != 'running':
                    get_cont.status = info
                    storage.new(get_cont)
                    storage.save()
                return redirect(url_for('appviews.home'))
            else:
                abort(404)
        else:
            abort(404)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        abort(404)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        abort(404)


@app_views.route("/containers/<username>", strict_slashes=False)
def statss(username):
    """
    get pre defined containers and those imported by you
    """
    print('username')
    containers = {}
    users = storage.get(User, username=username).to_dict()
    get_cont = storage.all(Container)
    print(get_cont)
    if get_cont:
        for key, value in get_cont.items():
            print(value.to_dict()['types'])
            if value.to_dict()['types'] is None or value.to_dict()['user_id'] == users['id']:
                print('yes')
                containers[value.to_dict()['name']] = value.to_dict()
            else:
                continue
        return jsonify(containers), 200
    else:
        abort(404)


@app_views.route('/containers/<username>/pull', strict_slashes=False, methods=['POST'])
def pull_containers(username):
    """
    pull container from Docker Hub
    """
    print('pull')
    data = request.form
    docker_id = data.get('docker_id')
    img_name = data.get('name')
    print(docker_id)
    print(img_name)
    img_data = {}
    if docker_id:
        full_image_name = f"{docker_id}/{img_name}:latest"
    else:
        full_image_name = f"{data['name']}:latest"

    api_url = f'http://52.87.212.95:2375/images/create?fromImage={full_image_name}'
    print(api_url)
    response = requests.post(api_url)

    if response.status_code == 200:
        api_url = 'http://52.87.212.95:2375/images/json'
        response = requests.get(api_url)
        print(response)

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
                    return redirect(url_for('appviews.home'))

            abort(404, description=f"Image '{full_image_name}' not found.")
    else:
        abort(404, description=response.text)


#@app_views.route("/containers/<username>", strict_slashes=False)
#def statss(username):
#    print(username)
#    return {
#        "users": storage.count(User),
#        "container": storage.count(Container)
#    }
