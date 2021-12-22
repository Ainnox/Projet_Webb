import sqlite3
from flask import Flask


def get_db_connection():
    conn = sqlite3.connect('project/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'maSuperClé'

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

