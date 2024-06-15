from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from wtforms.fields.simple import SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

from app.extensions import db, bcrypt
from app.models import User
from app.AIMS.user_forms import StudentForm

update_personal_information = Blueprint('update_personal_information', __name__)

class PersonalUpdateForm(StudentForm):
    submit = SubmitField('更新')

class PasswordResetForm(FlaskForm):
    old_password = PasswordField('請輸入原本的密碼', validators=[DataRequired()])
    new_password = PasswordField('重新輸入新密碼', validators=[DataRequired()])
    confirm_password = PasswordField('確認新密碼', validators=[DataRequired(), EqualTo('new_password', message='密碼不一致')])
    submit = SubmitField('變更密碼')

@update_personal_information.route('/update_personal_information', methods=['GET', 'POST'])
@login_required
def update_form():
    user = current_user
    form = PersonalUpdateForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('個人資料已更新', 'success')
        return redirect(url_for('update_personal_information.update_form'))
    
    return render_template('AIMS/update_personal_information.html', updateForm=form)

@update_personal_information.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = PasswordResetForm()
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
    return render_template('AIMS/reset_password.html', form=form)
