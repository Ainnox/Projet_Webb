from flask import Blueprint,render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login_ind.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')