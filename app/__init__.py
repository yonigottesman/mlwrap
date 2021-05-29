""" Main app """

from flask import Flask
from config import Config


def create_app(config_class=Config):
    """ Builder for app"""

    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.cluster import bp as wine_bp

    app.register_blueprint(wine_bp, url_prefix="/cluster")

    return app
