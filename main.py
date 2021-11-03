from flask import Blueprint, render_template, redirect, url_for, request, flash
from .__init__ import db
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from .passwordReset import ResetManager

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

        if ResetManager.resetPasswordForEmail(email=email, newPassword=password):
            flash('Successfully reset password.')
            return redirect(url_for('auth.login'))
        else:
            flash('Password reset was unsuccessful.')
            return redirect(url_for('main.reset'))
