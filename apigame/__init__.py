from time import sleep

from flask import Flask
from flask.logging import create_logger

from apigame.services.question_service import fetch_and_store_questions


def create_app():
    """
    Application factory for creating and configuring the Flask app.
    :return: Configured Flask app instance.
    """
    app = Flask(__name__)

    app.config.from_object("apigame.config.Config")

    logger = create_logger(app)
    logger.info("Starting Flask application...")

    from apigame.routes import register_blueprints
    register_blueprints(app)

    logger.info("Application setup complete.")
    logger.info("Fetching and storing questions...")
    sleep(5)
    fetch_and_store_questions()
    return app
