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
    return render_template('manage.html', name=current_user.name)

@main.route('/manage', methods=['GET'])
def manage_get():
    # login code goes here
    email = request.args.get('email')
    password = request.args.get('password')


    return redirect(url_for('main.manage'))
