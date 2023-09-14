#!/usr/bin/python3
"""
this is a view for users
"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import abort, request, jsonify, render_template, session, flash, redirect, url_for
import hashlib
import binascii
import os


def hash_password(password, salt=None):
    """
    hash user password
    """
    rounds = 100000
    hash_algo = hashlib.sha256()

    if salt is None:
        salt = os.urandom(16)
        hk = hashlib.pbkdf2_hmac(hash_algo.name, password.encode('utf-8'), salt, rounds)
        hashed_password = binascii.hexlify(hk).decode('utf-8')
        return {"passwd": hashed_password, "salt": salt}
    else:
        salt_bytes = binascii.unhexlify(salt)
        hk = hashlib.pbkdf2_hmac(hash_algo.name, password.encode('utf-8'), salt_bytes, rounds)
        hashed_password = binascii.hexlify(hk).decode('utf-8')
        return hashed_password


@app_views.route("/users", strict_slashes=False)
def get_all_users():
    """
    get all users in database
    """
    all_users = storage.all('User')
    user_list = []
    for value in all_users.values():
        user_list.append(value.to_dict())
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


@app_views.route("/signup", methods=['POST', 'GET'], strict_slashes=False)
def create_user():
    """
    create new user
    """
    if request.method == 'POST':
        data = {}
        form_data = request.form
        for key, value in form_data.items():
            data[key] = value

        if not form_data:
            return redirect(url_for('appviews.create_user'))

        if 'password' not in form_data:
            print('password')
            return redirect(url_for('appviews.create_user'))

        if 'email' not in form_data:
            print('email')
            return redirect(url_for('appviews.create_user'))

        hashed_pass = hash_password(data['password'])
        data['password'] = hashed_pass['passwd']
        data['salt'] = hashed_pass['salt']
        new_user = User(**data)
        new_user.save()
        return redirect(url_for('appviews.login_user'))
    else:
        return render_template('signup.html')


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
            if key == 'id' or key == 'email' or key == 'created_at' or key == 'updated_at' or key == 'username':
                pass
            else:
                if key == 'password':
                    user.password = hash_password(value)['passwd']
                    user.salt = hash_password(value)['salt']
                    updated = True
                elif key == 'first_name':
                    updated = True
                    user.first_name = value
                elif key == 'last_name':
                    updated = True
                    user.last_name = value
        if updated:
            storage.new(user)
            storage.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(400, description="Not a JSON")


@app_views.route("/login", strict_slashes=False, methods=['POST', 'GET'])
def login_user():
    """
    check passed password and username against password and
    username stored in database
    """
    if request.method == 'POST':
        user = storage.get(User, username=request.form['username'])
        if user:
            user_dict = user.to_dict()
            if user_dict['password'] == hash_password(request.form['password'], user_dict['salt']):
                session['user_id'] = user_dict['id']
                session['username'] = user_dict['username']
                return redirect(url_for('appviews.home'))
            else:
                return redirect(url_for('appviews.home'))
        else:
            return redirect(url_for('appviews.home'))
    else:
        return render_template('login.html')


@app_views.route('/logout', strict_slashes=False)
def logout():
    """
    logout from current session
    """
    session.clear()
    return redirect(url_for('appviews.login_user'))


@app_views.route("/home", strict_slashes=False)
def home():
    """
    on user login direct user to home screen with user's username and id 
    or redirect to login screen if login detailsare inaccurate
    """
    if 'user_id' in session:
        id = session.get('user_id')
        username = session.get('username')
        return render_template('container.html', id=id, username=username)
    else:
        flash('You need to log in to access this page.', 'danger')
        return redirect(url_for('appviews.login_user'))


@app_views.route("/", strict_slashes=False)
def landing_page():
    """
    direct user to the landing page
    """
    return render_template('landing.html')
