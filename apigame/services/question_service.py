from apigame.api.gpt_api import ChatGPTClient
from apigame.api.trivia_api import TriviaClient, default_request_config
from apigame.database.db import QuestionDB

question_db = QuestionDB()
trivia_client = TriviaClient()
gpt_client = ChatGPTClient()
default_request_config = default_request_config()


def fetch_and_store_questions() -> None:
    """
    Fetches trivia questions from an external source, processes them using GPT
    to add translations and hints, and stores them in the question database.
    """
    if question_db.get_question_count() >= 100:
        return None
    try:
        questions = trivia_client.get_questions(default_request_config)
        processed_questions = gpt_client.generate_translated_and_hinted_questions(questions)
        question_db.add_questions(processed_questions)
        print("Questions retrieved and processed!")
    except Exception as e:
        print(f"Error with fetch_and_store_questions: {e}")


def get_random_questions(amount):
    return question_db.get_random_questions(amount)


def get_question_by_id(question_id):
    return question_db.get_question_by_id(question_id)
