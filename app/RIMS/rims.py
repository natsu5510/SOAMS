from flask import Blueprint, render_template, url_for, redirect

rims = Blueprint('rims', __name__)

@rims.route('/')
def index():
    return render_template('/RIMS/rims.html')