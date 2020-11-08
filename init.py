"""
Initialize Flask App
"""

from flask import Flask

from config import app_config
from routes import movie_list_bp


def create_app(config):
    """
    Initialize Flask App

    :param str config: Environment Config
    :return: Created Flask App
    """
    # create flask app
    app = Flask(__name__)

    # get config name
    config_name = app_config[config]

    # set configuration
    app.config.from_object(config_name)

    # register blueprint
    app.register_blueprint(movie_list_bp)

    return app
