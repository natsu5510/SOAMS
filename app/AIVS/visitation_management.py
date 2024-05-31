from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.AIMS.login_management import role_required

visitation_management = Blueprint('visitation_management', __name__)

@visitation_management.route('/')
@login_required
def index():
    return render_template('/AIVS/visitation_management.html')