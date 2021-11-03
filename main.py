from flask import Blueprint, render_template, redirect, url_for, request, flash
from .__init__ import db
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from .passwordReset import ResetManager
from .models import User
import re

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/manage')
@login_required
def manage():
    if len(request.args) == 0:
        return render_template('manage.html', balance=current_user.balance)

    # login code goes here
    action = request.args.get('action')
    amount = request.args.get('amount')

    if action == "deposit":
        try:
            amount = float(amount)
            assert amount >= 0
            current_user.balance += amount
            db.session.commit()
        except:
            return render_template('manage.html', balance=current_user.balance)

    if action == "withdraw":
        try:
            amount = float(amount)
            assert amount >= 0
            assert current_user.balance >= amount
            current_user.balance -= amount
            db.session.commit()
        except:
            return render_template('manage.html', balance=current_user.balance)

    if action == "close":
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        return redirect(url_for('main.index'))


    return render_template('manage.html', balance=current_user.balance)

@main.route('/reset')
def reset():
    if len(request.args) <= 1:
        email = request.args.get('email')
        return render_template('reset.html', email=email)
    else:
        email = request.args.get('email')
        password = request.args.get('pass')
        confirm_pass = request.args.get('confirm-pass')
        # password validation with regex
        # Minimum eight characters, at least one upper case English letter, one lower case English letter, one number and one special character
        reg = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
	    # compiling regex
        pat = re.compile(reg)
	    # searching regex				
        mat = re.search(pat, password)
	    # validating conditions
        if not mat:
            flash("Password invalid.")
            return render_template('reset.html', email=email)

        if password != confirm_pass:
            flash('Passwords do not match.')
            return render_template('reset.html', email=email)
        elif ResetManager.resetPasswordForEmail(email=email, newPassword=password):
            flash('Successfully reset password.')
            return redirect(url_for('auth.login'))
        else:
            flash('Password reset was unsuccessful.')
            return redirect(url_for('main.reset'))

@main.route('/forgot-password')
def forgot_password():
    return render_template('forgot.html')

@main.route('/forgot')
def forgot():
    email = request.args.get('user')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if not user:
        flash('No matching account found.')
        return render_template('forgot.html')
    else:
        ResetManager.sendEmailForReset(email)
        flash('Please check your email for instructions on resetting your password.')
        return render_template('forgot.html')

