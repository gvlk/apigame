from time import sleep

from flask import Flask

from apigame.api.trivia_api import default_request_config
from apigame.services.question_service import fetch_and_store_questions


def create_app() -> Flask:
    """
    Application factory for creating and configuring the Flask app.
    :return: Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object("apigame.config.Config")

    app.logger.info("Creating Flask application instance.")

    from apigame.routes import register_blueprints
    register_blueprints(app)
    app.logger.info("Routes registered successfully.")

    app.logger.info("Starting the question-fetching service.")
    try:
        fetch_and_store_questions()
        sleep(10)
        fetch_and_store_questions()
        sleep(10)
    except Exception as e:
        app.logger.error(f"An error occurred while fetching questions: {e}")

    return app
