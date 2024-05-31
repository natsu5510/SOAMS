from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.AIMS.login_management import role_required

rental_information_exchange = Blueprint('rental_information_exchange', __name__)

@rental_information_exchange.route('/')
@login_required
def index():
    return render_template('/RIMS/rental_information_exchange.html')