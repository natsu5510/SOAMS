from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.AIMS.login_management import role_required

rental_advertisement = Blueprint('rental_advertisement', __name__)

@rental_advertisement.route('/')
@login_required
def index():
    return render_template('/RIMS/rental_advertisement.html')