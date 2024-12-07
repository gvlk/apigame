from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return render_template('index.html', message="Hello, Flask!")

@main.route('/play')
def play():
    return ""

@main.route('/ranking')
def ranking():
    return ""

@main.route('/avatar')
def avatar():
    return ""