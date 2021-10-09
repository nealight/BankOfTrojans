from flask import Blueprint, render_template, redirect, url_for, request, flash
from __init__ import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/manage')
@login_required
def manage():
    action = request.args.get('action')
    amount = request.args.get('amount')
    if action and amount:
        return manage_get()
    return render_template('manage.html', balance=current_user.balance)

@main.route('/manage', methods=['GET'])
def manage_get():
    # login code goes here
    action = request.args.get('action')
    amount = request.args.get('amount')

    if action == "deposit":
        current_user.balance += float(amount)
        db.session.commit()


    return redirect(url_for('main.manage'))
