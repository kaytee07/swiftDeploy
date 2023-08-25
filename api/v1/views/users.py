#!/usr/bin/python3
"""
this is a view for users
"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import abort, request, jsonify


@app_views.route("/users", strict_slashes=False)
def get_all_users():
    """
    get all users in database
    """
    all_users = storage.all('User')
    user_list = []
    for value in all_users.values():
        user_list.append(value.to_dict())
    print(user_list)
    return jsonify(user_list), 200


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id):
    """
    get user based on user_id passed
    """
    if storage.get(User, user_id):
        return storage.get(User, user_id).to_dict()
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    delete_user from database
    """
    if storage.get(User, user_id):
        obj = storage.get(User, user_id)
        storage.delete(obj)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'password' not in data:
        abort(400, description="Missing password")

    if 'email' not in data:
        abort(400, description="Missing email")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """
    update user data stored in the database
    """
    updated = False
    updates = request.get_json()
    user = storage.get(User, user_id)
    if user:
        for key, value in updates.items():
            if key == 'id' or key == 'email' or key == 'created_at' or key == 'updated_at' or key == 'last_name' or key == 'first_name':
                pass
            else:
                if key == 'password':
                    user.password = value
                    updated = True
                elif key == 'username':
                    updated = True
                    user.username = value
        if updated:
            storage.new(user)
            storage.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(400, description="Not a JSON")


@app_views.route("/users/login", strict_slashes=False, methods=['POST'])
def login_user():
    """
    check passed password and username against password and
    username stored in database
    """
    data = request.get_json()
    user = storage.get(User, username=data['username'])
    if user:
        user_dict = user.to_dict()
        if user_dict['password'] == data['password']:
            return jsonify({
                "password": user_dict['password'],
                "login": "successfully"
            }), 200
        else:
            abort(404, description="incorrect username or password")
    else:
        abort(404, description="User not found")
