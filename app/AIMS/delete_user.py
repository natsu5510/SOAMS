from flask import Blueprint, flash, render_template, url_for, redirect
from flask_login import login_required, current_user
from wtforms.fields.simple import SubmitField

from app import db
from app.AIMS.user_forms import AdministratorForm, AdvisorForm, StudentForm, LandlordForm
from app.models import User

delete_user = Blueprint('delete_user', __name__)


class AdministratorDeleteForm(AdministratorForm):
    submit = SubmitField('確認刪除')


class AdvisorDeleteForm(AdvisorForm):
    submit = SubmitField('確認刪除')


class StudentDeleteForm(StudentForm):
    def __init__(self, *args, **kwargs):
        super(StudentDeleteForm, self).__init__(*args, **kwargs)
        self.advisor_id.choices = [(advisor.id, advisor.name) for advisor in User.query.filter_by(type='advisor').all()]
    submit = SubmitField('確認刪除')


class LandlordDeleteForm(LandlordForm):
    submit = SubmitField('確認刪除')


@delete_user.route('/delete_user/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_form(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash('查無使用者', 'warning')
        return render_template('AIMS/delete_user.html')
    elif user == current_user:
        flash('無法刪除正在使用的管理員帳號', 'danger')
        return render_template('AIMS/delete_user.html')

    if user.type == 'administrator':
        form = AdministratorDeleteForm(obj=user)
    elif user.type == 'advisor':
        form = AdvisorDeleteForm(obj=user)
    elif user.type == 'student':
        form = StudentDeleteForm(obj=user)
    elif user.type == 'landlord':
        form = LandlordDeleteForm(obj=user)
    else:
        flash('欲刪除的使用者身分錯誤', 'warning')
        return render_template('AIMS/delete_user.html')

    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash('使用者刪除成功', 'success')
        return redirect(url_for('search_user_information.delete_search_form'))

    return render_template('AIMS/delete_user.html', deleteForm=form)
