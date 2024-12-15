from flask import Blueprint, render_template, request, jsonify, session, redirect

from apigame.services.question_service import get_random_questions, get_question_by_id
from apigame.services.session_service import start_game_session, update_session, end_game_session
from apigame.services.user_service import get_user_by_username

game = Blueprint('game', __name__)


@game.route('/solo', methods=['GET', 'POST'])
def solo():
    """
    Handles solo trivia gameplay.
    """
    username = session.get('username')
    if not username:
        return redirect('/')

    user = get_user_by_username(username)
    if not user:
        return redirect('/')

    if request.method == 'GET':
        questions = get_random_questions(3)
        session_id = start_game_session(user['user_id'], [q['hash_id'] for q in questions])
        session['session_id'] = session_id
        return render_template('solo_play.html', questions=questions)

    elif request.method == 'POST':
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({"error": "Session not found"}), 404

        data = request.get_json()
        question_id = data.get('questionId')
        selected_answer = data.get('selectedAnswer')

        question = get_question_by_id(question_id)
        if question:
            correct = question['correct_answer'] == selected_answer
            update_session(session_id, question_id, correct)
            return jsonify({"isCorrect": correct, "correctAnswer": question['correct_answer']}), 200

        return jsonify({"error": "Question not found"}), 404


@game.route('/results', methods=['GET'])
def results():
    """
    Displays results after a game session.
    """
    session_id = session.get('session_id')
    if session_id:
        end_game_session(session_id)
        correct, total = end_game_session(session_id)
        return render_template('results.html', correct_answers=correct, total_questions=total)
    return redirect('/')
