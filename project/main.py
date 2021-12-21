from flask import Blueprint,render_template, session
from . import get_db_connection

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('login_ind.html')


@main.route('/profile')
def profile():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT name FROM users WHERE email=?', [session['email']])
    con.commit()
    query = cur.fetchone()
    con.close()
    session['name'] = query[0]
    return render_template('profile.html')
