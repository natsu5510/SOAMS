from flask import Blueprint, render_template

aivs = Blueprint('aivs', __name__)

@aivs.route('/')
def index():
    return render_template('/AIVS/aivs.html')