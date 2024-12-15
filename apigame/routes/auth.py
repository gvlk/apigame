from flask import Blueprint, request, session, redirect

from apigame.services.user_service import authenticate_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    """
    Log in the user by verifying credentials.
    """
    username = request.form['username']
    password = request.form['password']
    if authenticate_user(username, password):
        session['username'] = username
    return redirect('/')


@auth.route('/logout')
def logout():
    """
    Log out the user by clearing the session.
    """
    session.pop('username', None)
    return redirect('/')
