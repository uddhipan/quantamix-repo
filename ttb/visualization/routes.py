from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from ttb import db, bcrypt
from datetime import datetime
from ttb.models import User, Post, Follow


visualization = Blueprint('visualization', __name__)

@visualization.route("/overview")
def overview():

    return render_template('overview.html',title='Overvew')

# Text analysis part temporary
@visualization.route("/index")
def index():
	return render_template('index.html')
