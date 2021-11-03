from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from .__init__ import db
from flask_login import login_user, logout_user, login_required
from .passwordReset import ResetManager

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    if len(request.args) == 0:
        return render_template('login.html')

    email = request.args.get('user')
    password = request.args.get('pass')

    if request.args.get('reset'):
        ResetManager.sendEmailForReset(email)
        flash('Please check your email for instructions on resetting your password.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=True)
    return redirect(url_for('main.manage'))

@auth.route('/register')
def signup():
    if len(request.args) == 0:
        return render_template('register.html')

    email = request.args.get('user')
    password = request.args.get('pass')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, balance=0.0, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



