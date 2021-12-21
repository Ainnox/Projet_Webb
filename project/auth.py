import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request, flash
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    con = sqlite3.connect('project/database.db')
    cur = con.cursor()
    cur.execute('SELECT password FROM users WHERE email=?', [email])
    query = cur.fetchone()
    con.commit()

    if check_password_hash(password, query):
        return redirect(url_for('main.profile'))
    else:
        flash()


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password').encode('utf-8')

    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)

    con = sqlite3.connect('project/database.db')
    cur = con.cursor()
    cur.execute('SELECT email FROM users')
    user = cur.fetchone()
    con.commit()

    if user:
        flash("This email already exist")
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
    return 'Logout'
