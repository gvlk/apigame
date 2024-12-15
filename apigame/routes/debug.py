from flask import Blueprint

from apigame.services.question_service import question_db
from apigame.services.session_service import session_db
from apigame.services.user_service import user_db

debug = Blueprint('debug', __name__)


@debug.route('/user')
def debug_user():
    return user_db.users.to_dict()


@debug.route('/session')
def debug_session():
    return session_db.sessions.to_dict()


@debug.route('/question')
def debug_question():
    return question_db.questions.to_dict()
