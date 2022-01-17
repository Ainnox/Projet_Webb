from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import bcrypt
from . import get_db_connection

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form.get('password').encode('utf-8')
    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT password,name FROM users WHERE email=?', [email])
    con.commit()
    query = cur.fetchone()
    con.close()

    if bcrypt.checkpw(password, query[0]):
        session['email'] = email
        session['name'] = query[1]
        return redirect(url_for('main.index'))
    flash("Wrong password")

    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=('GET', 'POST'))
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password').encode('utf-8')

    if not email:
        flash("Please enter your email", 'error')
        return redirect(url_for('auth.signup'))
    elif not name:
        flash("Please enter a name", 'error')
        return redirect(url_for('auth.signup'))
    elif not password:
        flash("Please enter a password", 'error')
        return redirect(url_for('auth.signup'))

    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)

    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT email FROM users WHERE email=?', [email])
    user = cur.fetchone()

    if user:
        flash("This email already exist", 'error')
        return redirect(url_for('auth.login'))

    cur.execute("SELECT id_role FROM Role WHERE role_name='guest'")
    new_user = [
        email,
        name,
        hashed,
        cur.fetchone()[0]
    ]

    cur.execute('INSERT INTO users (email,name,password,id_role) VALUES (? ,? ,?,?)', new_user)
    con.commit()
    con.close()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('main.index'))
