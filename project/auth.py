import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
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
    cur.execute('SELECT password,name,admin FROM users WHERE email=?', [email])
    con.commit()
    query = cur.fetchone()
    con.close()

    if bcrypt.checkpw(password, query[0]):
        session['email'] = email
        session['name'] = query[1]
        session['admin'] = query[2]
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

    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)

    con = get_db_connection()
    cur = con.cursor()
    cur.execute('SELECT email FROM users WHERE email=?', [email])
    con.commit()
    user = cur.fetchone()

    if user:
        flash("This email already exist", 'error')
        return redirect(url_for('auth.login'))

    new_user = [
        email,
        name,
        hashed
    ]

    cur.execute('INSERT INTO users (email,name,password) VALUES (? ,? ,?)', new_user)
    con.commit()
    con.close()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('admin', None)
    return redirect(url_for('main.index'))
