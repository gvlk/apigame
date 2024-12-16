from apigame.database.db import SessionDB

session_db = SessionDB()


def start_game_session(user_id, question_ids):
    return session_db.start_session(user_id, question_ids)


def update_session(session_id, question_id, correct):
    session_db.answer_question(session_id, question_id, correct)


def end_game_session(session_id):
    return session_db.get_correct_answer_count(session_id)


def get_player_ranking():
    return session_db.get_player_ranking()
