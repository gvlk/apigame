from apigame.api.trivia_api import TriviaClient, default_request_config
from apigame.database.db import QuestionDB

question_db = QuestionDB()
trivia_client = TriviaClient()
default_request_config = default_request_config()


def fetch_and_store_questions() -> None:
    try:
        questions = trivia_client.get_questions(default_request_config)
        question_db.add_questions(questions)
    except Exception as e:
        print(e)


def get_random_questions(amount):
    return question_db.get_random_questions(amount)


def get_question_by_id(question_id):
    return question_db.get_question_by_id(question_id)
