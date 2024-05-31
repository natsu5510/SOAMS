from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.AIMS.login_management import role_required

accommodation_management = Blueprint('accommodation_management', __name__)

@accommodation_management.route('/')
@login_required
def index():
    return render_template('/AIVS/accommodation_management.html')