from apigame.api.trivia_api import TriviaClient
from apigame.database.db import QuestionDB

question_db = QuestionDB()
trivia_client = TriviaClient()


def fetch_and_store_questions(amount: int = 3):
    try:
        questions = trivia_client.get_questions(amount=amount)
        question_db.add_question(questions)
    except Exception as e:
        print(e)


def get_random_questions(amount):
    return question_db.get_random_questions(amount)


def get_question_by_id(question_id):
    return question_db.get_question_by_id(question_id)
