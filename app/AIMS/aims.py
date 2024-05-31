from flask import Blueprint, render_template

aims = Blueprint('aims', __name__)

@aims.route('/')
def index():
    return render_template('/AIMS/aims.html')