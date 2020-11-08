"""
Movie List Application
"""

from flask import render_template, session, current_app, Blueprint
from services.movies_api_services import MoviesAPIServices

# set blueprint
movie_list_bp = Blueprint('movie_list_bp', __name__)


@movie_list_bp.route('/', methods=['GET'])
def index():
    """
    Index
    """
    return 'Go to /movies route to display movie list'


@movie_list_bp.route('/movies/', methods=['GET'])
def display_movies():
    """
    Route to display movies - characters table
    """
    try:
        # get movies from session if already stored
        if session.get('movies_characters'):
            movies_characters = session['movies_characters']
        else:
            # initialize movies api service
            movies_api_services = MoviesAPIServices(api_base_url=current_app.config['API_BASE_URL'],
                                                    movies_endpoint=current_app.config['API_MOVIES_ENDPOINT'],
                                                    people_endpoint=current_app.config['API_PEOPLE_ENDPOINT'],
                                                    results_limit=current_app.config['API_MAX_RESULTS'])
            # get movies and characters from API
            movies = movies_api_services.get_movies()
            characters = movies_api_services.get_characters()
            # get combined movies info
            movies_characters = movies_api_services.get_movies_characters_combination(movies=movies,
                                                                                      characters=characters)
            # store movies in session
            session['movies_characters'] = movies_characters
        return render_template('movies.html', movies=movies_characters)
    except Exception as e:
        current_app.logger.error(e)
