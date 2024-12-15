from typing import TypedDict


class Question(TypedDict):
    category: str
    difficulty: str
    type: str
    question: str
    correct_answer: str
    incorrect_answers: tuple[str]
    hint: str
