from datetime import datetime
from typing import TypedDict, Iterable

import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

from apigame.api.trivia_api import Question


class Session(TypedDict):
    session_id: int
    user_id: str
    start_time: int
    end_time: int
    questions: dict[str, bool]


class QuestionDB:
    def __init__(self):
        # Initialize an empty DataFrame with columns based on the question format
        self.questions = pd.DataFrame(columns=tuple(Question.__annotations__.keys()))

    def add_questions(self, questions: Iterable[Question]) -> None:
        """Adds new questions to the DataFrame."""

        new_rows = pd.DataFrame(questions)
        self.questions = pd.concat([self.questions, new_rows], ignore_index=True)

    def get_question_by_id(self, hash_id: str) -> Question | None:
        """Retrieve a question by its hash_id."""
        question = self.questions[self.questions['hash_id'] == hash_id]
        if not question.empty:
            return question.iloc[0].to_dict()
        return None

    def get_random_questions(self, amount: int) -> list[Question]:
        """
        Retrieve N random questions from the database.

        :param amount: The number of random questions to retrieve.
        :return: A list of random questions as dictionaries.
        """
        if self.questions.empty:
            return []
        # Use Pandas' sample method to get random rows
        random_questions = self.questions.sample(n=min(amount, len(self.questions)), replace=False)
        return random_questions.to_dict(orient='records')


class SessionDB:
    def __init__(self):
        # Initialize an empty DataFrame to store session data
        self.sessions = pd.DataFrame(columns=tuple(Session.__annotations__.keys()))

    def _generate_session_id(self) -> int:
        """Generate a unique session ID."""
        return len(self.sessions) + 1

    def start_session(self, user_id: str, question_ids: Iterable[str]) -> int:
        """Start a new quiz session for the user."""
        session_id = self._generate_session_id()
        start_time = datetime.now()

        # Add the new session to the DataFrame
        new_session = {
            "session_id": session_id,
            "user_id": user_id,
            "start_time": start_time,
            "end_time": int(),
            "questions": {q_id: False for q_id in question_ids},
        }

        new_session_df = pd.DataFrame([new_session])
        self.sessions = pd.concat([self.sessions, new_session_df], ignore_index=True)
        return session_id

    def end_session(self, session_id: str) -> None:
        """End the quiz session and store the results."""
        end_time = datetime.now()
        session = self.sessions[self.sessions["session_id"] == session_id]
        if not session.empty:
            self.sessions.loc[self.sessions["session_id"] == session_id, "end_time"] = end_time

    def get_session(self, session_id: str) -> Session | None:
        """Retrieve session information by session_id."""
        session = self.sessions[self.sessions["session_id"] == session_id]
        if not session.empty:
            return session.iloc[0].to_dict()
        return None

    def get_user_sessions(self, user_id: str) -> pd.DataFrame:
        """Get all sessions for a specific user."""
        return self.sessions[self.sessions["user_id"] == user_id]

    def get_all_sessions(self) -> pd.DataFrame:
        """Get all session records."""
        return self.sessions

    def answer_question(self, session_id: str, question_id: str, correct: bool) -> None:
        session = self.sessions[self.sessions["session_id"] == session_id]
        if not session.empty:
            # Update the 'questions' dictionary with the answer to the current question
            questions = session.iloc[0]['questions']
            questions[question_id] = correct

    def delete_session(self, session_id: str) -> None:
        """Delete a session from the database."""
        self.sessions = self.sessions[self.sessions["session_id"] != session_id]

    def get_correct_answer_count(self, session_id: str) -> tuple[int, int]:
        """Return the count of correct answers and total questions for a session."""
        session = self.sessions[self.sessions["session_id"] == session_id]
        if not session.empty:
            questions = session.iloc[0]['questions']
            correct_count = sum(questions.values())
            total_count = len(questions)
            return correct_count, total_count
        return 0, 0


class UserDB:
    def __init__(self):
        self.users = pd.DataFrame(columns=["user_id", "username", "password_hash"])

    def create_new_user(self, username: str, password: str) -> bool:
        """Register a new user. Returns False if username already exists."""
        if username in self.users["username"].values:
            return False
        password_hash = generate_password_hash(password)
        new_user = pd.DataFrame([{
            "user_id": len(self.users) + 1,
            "username": username,
            "password_hash": password_hash,
        }])
        self.users = pd.concat([self.users, new_user], ignore_index=True)
        return True

    def check_user_credentials(self, username: str, password: str) -> bool:
        """Validate username and password for login."""
        user = self.users[self.users["username"] == username]
        if not user.empty:
            return check_password_hash(user.iloc[0]["password_hash"], password)
        return self.create_new_user(username, password)

    def get_user_by_username(self, username: str) -> dict | None:
        """Retrieve user information by username."""
        user = self.users[self.users["username"] == username]
        if not user.empty:
            return user.iloc[0].to_dict()
        return None
