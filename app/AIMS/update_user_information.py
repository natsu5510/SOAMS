from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from wtforms.fields.simple import SubmitField

from app import db
from app.AIMS.user_forms import AdvisorForm, StudentForm, LandlordForm
from app.models import User

update_user_information = Blueprint('update_user_information', __name__)


class AdvisorUpdateForm(AdvisorForm):
    submit = SubmitField('送出')


class StudentUpdateForm(StudentForm):
    submit = SubmitField('送出')


class LandlordUpdateForm(LandlordForm):
    submit = SubmitField('送出')


@update_user_information.route('/update_user_information/<user_id>', methods=['GET', 'POST'])
@login_required
def update_form(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('查無使用者', 'warning')
        return render_template('AIMS/update_user_information.html')

    if user.type == 'advisor':
        form = AdvisorUpdateForm(obj=user)
    elif user.type == 'student':
        form = StudentUpdateForm(obj=user)
    elif user.type == 'landlord':
        form = LandlordUpdateForm(obj=user)
    else:
        flash('欲修改的使用者身分錯誤', 'warning')
        return render_template('AIMS/update_user_information.html')

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('使用者資料已更新', 'success')
        return render_template('AIMS/update_user_information.html', user_id=user_id)
    elif form.is_submitted():
        flash('修改失敗，請檢查您的輸入', 'danger')
        return render_template('AIMS/update_user_information.html', updateForm=form)

    return render_template('AIMS/update_user_information.html', updateForm=form)
