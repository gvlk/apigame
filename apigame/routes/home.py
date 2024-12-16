from flask import render_template, Blueprint

from apigame.services.session_service import get_player_ranking
from apigame.services.user_service import format_ranking_table

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home.html')


@home.route('/ranking')
def ranking():
    """
    Fetch the player ranking DataFrame, format it to replace user IDs with usernames,
    and pass it to the template for rendering.
    """
    ranking_df = get_player_ranking()
    formatted_ranking_df = format_ranking_table(ranking_df)
    ranking_html = formatted_ranking_df.to_html(index=False, header=False,
                                                classes="table table-bordered table-hover table-striped")
    return render_template('ranking.html', ranking_html=ranking_html)
