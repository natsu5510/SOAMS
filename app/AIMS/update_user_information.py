from flask import Blueprint, render_template, flash
from flask_login import login_required
from wtforms.fields.simple import SubmitField

from app.AIMS.user_forms import AdvisorForm, StudentForm, LandlordForm
from app.models import User

update_user_information = Blueprint('update_user_information', __name__)


class AdvisorUpdateForm(AdvisorForm):
    submit = SubmitField('查詢')


class StudentUpdateForm(StudentForm):
    submit = SubmitField('查詢')


class LandlordUpdateForm(LandlordForm):
    submit = SubmitField('查詢')


@update_user_information.route('/update_user_information/<user_id>', methods=['GET', 'POST'])
@login_required
def update_form(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('查無使用者', 'warning')
        return render_template('AIMS/update_user_information.html', updateForm=None)

    if user.type == 'advisor':
        form = AdvisorUpdateForm(obj=user)
    elif user.type == 'student':
        form = StudentUpdateForm(obj=user)
    elif user.type == 'landlord':
        form = LandlordUpdateForm(obj=user)
    else:
        flash('欲修改的使用者身分錯誤', 'warning')
        return render_template('AIMS/update_user_information.html', updateForm=None)

    if form.validate_on_submit():
        pass

    return render_template('AIMS/update_user_information.html', updateForm=form, user=user)
