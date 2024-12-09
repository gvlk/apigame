from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def homepage():
    return render_template('home.html')


@main.route('/play')
def play():
    return ""


@main.route('/ranking')
def ranking():
    return ""


@main.route('/avatar')
def avatar():
    return ""
