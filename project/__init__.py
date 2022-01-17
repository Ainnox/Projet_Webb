import sqlite3
from flask import Flask, session


def get_db_connection():
    conn = sqlite3.connect('project/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_perm(right):
    co = get_db_connection()
    cur = co.cursor()
    cur.execute("SELECT rights_name FROM Users NATURAL JOIN Role NATURAL JOIN Posses NATURAL JOIN RIGHTS WHERE email=?",
                (session.get('email'),))
    rights = cur.fetchall()
    co.close()
    for r in rights:
        print(r[0])
        if r[0] == right:
            return True
    return False


def get_role(need_role):
    co = get_db_connection()
    cur = co.cursor()
    cur.execute("SELECT role_name FROM Users NATURAL JOIN Role WHERE email=?",
                (session.get('email'),))
    role = cur.fetchone()
    co.close()
    if role and role[0] == need_role:
        return True
    else:
        return False


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'maSuperClé'

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.jinja_env.globals.update(get_role=get_role)
    app.jinja_env.globals.update(get_perm=get_perm)

    return app
