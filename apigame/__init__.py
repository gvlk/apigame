from flask import Flask


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object('apigame.config.Config')

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app