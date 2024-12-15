import hashlib
from html import unescape
from random import shuffle
from typing import TypedDict

from requests import get as requests_get


class Question(TypedDict):
    hash_id: str
    category: str
    difficulty: str
    type: str
    question: str
    correct_answer: str
    incorrect_answers: tuple[str]
    shuffled_answers: tuple[str]


class TriviaClient:
    def __init__(self):
        self.base_url = "https://opentdb.com"
        self.token = self._get_new_token()

    def _get_new_token(self, reset: bool = False) -> str:
        """Fetches a new session token for the API."""
        token_url = f"{self.base_url}/api_token.php?command="
        if reset:
            token_url += f"reset&token={self.token}"
        else:
            token_url += "request"
        response = requests_get(token_url).json()
        if response.get("response_code") == 0:
            return response["token"]
        else:
            raise Exception("Failed to retrieve token.")

    @staticmethod
    def _generate_question_hash(question: str, correct_answer: str, incorrect_answers: list[str]) -> str:
        """Generate a consistent hash ID for a question."""
        text = question + correct_answer + "".join(incorrect_answers)
        return hashlib.sha256(text.encode()).hexdigest()

    def _process_questions(self, questions: list[dict]) -> list[Question]:
        """
        Processes questions by unescaping text and shuffling the answers.

        :param questions: A list of questions fetched from the API.
        :return: The processed list of questions, where 'incorrect_answers' and 'shuffled_answers' are tuples.
        """
        for question in questions:
            question["question"] = unescape(question["question"])
            question["correct_answer"] = unescape(question["correct_answer"])
            question["incorrect_answers"] = tuple(unescape(answer) for answer in question["incorrect_answers"])

            all_answers = list(question["incorrect_answers"]) + [question["correct_answer"]]
            shuffle(all_answers)
            question["shuffled_answers"] = tuple(all_answers)

            question["hash_id"] = self._generate_question_hash(question["question"], question["correct_answer"],
                                                               question["incorrect_answers"])

        return questions

    def get_questions(
            self,
            amount: int,
            category: int | None = None,
            difficulty: str | None = None,
            q_type: str | None = None
    ) -> list[Question]:
        """
        Fetches trivia questions from the API.

        :param amount: Number of questions to fetch.
        :param category: Category ID for filtering questions, or None for all categories.
        :param difficulty: Difficulty level ('easy', 'medium', 'hard'), or None for all difficulties.
        :param q_type: Type of questions ('multiple', 'boolean'), or None for all types.
        :return: A list of questions, each as a dictionary containing the question text, answers, and other metadata.
        """

        params = {
            "token": self.token,
            "amount": amount,
        }
        if category is not None:
            params["category"] = category
        if difficulty is not None:
            params["difficulty"] = difficulty
        if q_type is not None:
            params["q_type"] = q_type

        url = f"{self.base_url}/api.php"
        response = requests_get(url, params=params).json()

        response_code = response.get("response_code")
        if response_code == 0:
            return self._process_questions(response["results"])
        elif response_code == 4:  # Token exhausted
            self._get_new_token(True)
            return self.get_questions(amount, category, difficulty, q_type)
        else:
            raise Exception(f"Failed to fetch questions. Response code = {response_code}")

    def get_categories(self):
        """
        Fetches available trivia categories from the API.
        """
        category_url = f"{self.base_url}/api_category.php"
        response = requests_get(category_url).json()
        if response.get("trivia_categories"):
            return response["trivia_categories"]
        else:
            raise Exception("Failed to fetch categories.")
