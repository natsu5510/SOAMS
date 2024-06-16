from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

from app.AIMS.user_forms import StudentForm, AdvisorForm, LandlordForm
from app.extensions import db, bcrypt

update_personal_information = Blueprint('update_personal_information', __name__)


class StudentUpdateForm(StudentForm):
    submit = SubmitField('確認更改')


class AdvisorUpdateForm(AdvisorForm):
    submit = SubmitField('確認更改')


class LandlordUpdateForm(LandlordForm):
    submit = SubmitField('確認更改')


class PasswordUpdateForm(FlaskForm):
    old_password = PasswordField('請輸入原本的密碼', validators=[DataRequired()])
    new_password = PasswordField('重新輸入新密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認新密碼',
                                     validators=[DataRequired(), EqualTo('new_password', message='密碼不一致')])
    submit = SubmitField('變更密碼')


@update_personal_information.route('/update_personal_information', methods=['GET', 'POST'])
@login_required
def update_form():
    user = current_user

    if user.type == 'student':
        form = StudentUpdateForm(obj=user)
    elif user.type == 'advisor':
        form = AdvisorUpdateForm(obj=user)
    elif user.type == 'landlord':
        form = LandlordUpdateForm(obj=user)
    else:
        flash('使用者身分錯誤', 'danger')
        return render_template('AIMS/update_personal_information.html')

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('個人資料已更新', 'success')
        return render_template('AIMS/update_personal_information.html')

    return render_template('AIMS/update_personal_information.html', updateForm=form)


@update_personal_information.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.passwd, form.old_password.data):
            flash('原本的密碼不正確', 'danger')
        elif form.new_password.data != form.confirm_password.data:
            flash('輸入的密碼不一致，請重新輸入', 'danger')
        elif form.new_password.data == form.old_password.data:
            flash('新密碼與原密碼一樣，請再重新輸入', 'danger')
        else:
            current_user.passwd = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('密碼已成功更改', 'success')
            return redirect(url_for('update_personal_information.update_form'))

    return render_template('AIMS/update_password.html', form=form)
