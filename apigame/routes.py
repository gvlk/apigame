from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from apigame.api.trivia_api import TriviaClient
from apigame.database.db import QuestionDB, SessionDB, UserDB

main = Blueprint('main', __name__)

trivia_client = TriviaClient()
user_db = UserDB()
question_db = QuestionDB()
session_db = SessionDB()
try:
    for q in trivia_client.get_questions(amount=5):
        question_db.add_question(q)
except Exception as e:
    pass


@main.route('/')
def homepage():
    return render_template('home.html')


@main.route('/solo-play', methods=['GET', 'POST'])
def solo_play():
    """
    Fetch trivia questions and display them one at a time for the player.
    The player will select an answer, and the next question will appear.
    """

    username = session['username']
    user = user_db.get_user_by_username(username)
    if not user:
        return redirect(url_for('main.homepage'))

    user_id = user['user_id']

    if request.method == 'GET':
        amount = 3
        questions = question_db.get_random_questions(amount)

        session_id = session_db.start_session(user_id, tuple(question["hash_id"] for question in questions))

        # Store session_id in Flask's session or cookies for later use
        session['session_id'] = session_id

        return render_template('solo_play.html', questions=questions)

    elif request.method == 'POST':
        data = request.get_json()

        session_id = session.get('session_id')
        if not session_id:
            return jsonify({"error": "Session not found"}), 404

        question_id = data.get('questionId')
        selected_answer = data.get('selectedAnswer')

        # Get the question from the database
        question = question_db.get_question_by_id(question_id)
        if question:
            correct = question['correct_answer'] == selected_answer

            # Update the session with the result of the current question
            session_db.answer_question(session_id, question_id, correct)

            result = {
                "questionId": question_id,
                "isCorrect": correct,
                "correctAnswer": question['correct_answer'],
            }

            return jsonify(result), 200
        else:
            return jsonify({"error": "Question not found", "questionId": question_id}), 404


@main.route("/results", methods=['GET'])
def results():
    """
    Display the quiz results after the game is completed.
    """
    if request.method == 'GET':
        session_id = session.get('session_id')
        session_db.end_session(session_id)
        correct_answers, total_questions = session_db.get_correct_answer_count(session_id)

        return render_template('results.html', correct_answers=correct_answers, total_questions=total_questions)


@main.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if user_db.check_user_credentials(username, password):
            session['username'] = username
        return redirect(url_for('main.homepage'))


@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@main.route('/debug-user')
def debug_user():
    return user_db.users.to_dict()


@main.route('/debug-session')
def debug_session():
    return session_db.sessions.to_dict()


@main.route('/debug-question')
def debug_question():
    return question_db.questions.to_dict()


@main.route('/ranking')
def ranking():
    return ""


@main.route('/avatar')
def avatar():
    return ""
