import threading
from time import sleep

from flask import Flask
from flask.logging import create_logger

from apigame.api.trivia_api import default_request_config
from apigame.services.question_service import fetch_and_store_questions


def fetch_and_store_questions_periodically() -> None:
    """
    Fetches and stores questions in the database every few seconds.
    This function runs in a separate thread to ensure it does not block the main Flask application.
    """
    while True:
        fetch_and_store_questions()
        sleep(10)


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

    logger.info("Starting background thread for fetching and storing questions...")
    thread = threading.Thread(target=fetch_and_store_questions_periodically, daemon=True)
    thread.start()

    logger.info("Application setup complete.")

    return app
