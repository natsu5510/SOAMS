from flask import Blueprint, render_template
from flask_login import login_required

update_personal_information = Blueprint('update_personal_information', __name__)


@update_personal_information.route('/update_personal_information', methods=['GET', 'POST'])
@login_required
def update_form():
    return render_template('AIMS/update_personal_information.html')
