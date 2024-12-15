from .auth import auth
from .debug import debug
from .game import game
from .home import home


def register_blueprints(app):
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(debug, url_prefix='/debug')
    app.register_blueprint(game, url_prefix='/game')
    app.register_blueprint(home, url_prefix='/')
