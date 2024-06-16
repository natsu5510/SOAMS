from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import DataRequired

from app import bcrypt, db
from app.AIMS.user_forms import AdvisorForm, StudentForm, LandlordForm
from app.models import User

create_user = Blueprint('create_user', __name__)


class UserTypeForm(FlaskForm):
    user_type = SelectField('使用者身分',
                            choices=[('', '請選擇'), ('advisor', '導師'), ('student', '學生'), ('landlord', '房東')],
                            validators=[DataRequired()], default='')
    submit = SubmitField('確認')


class AdvisorCreateForm(AdvisorForm):
    type = HiddenField('使用者身分', default='advisor', validators=[DataRequired(message='* 此欄位不可為空')])
    submit = SubmitField('新增')


class StudentCreateForm(StudentForm):
    type = HiddenField('使用者身分', default='student', validators=[DataRequired(message='* 此欄位不可為空')])
    submit = SubmitField('新增')


class LandlordCreateForm(LandlordForm):
    type = HiddenField('使用者身分', default='landlord', validators=[DataRequired(message='* 此欄位不可為空')])
    submit = SubmitField('新增')


@create_user.route('/create_user_type', methods=['GET', 'POST'])
@login_required
def user_type_form():
    form = UserTypeForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        return redirect(url_for('create_user.create_form', user_type=user_type))

    return render_template('AIMS/create_user_type.html', typeForm=form)


@create_user.route('/create_user/<user_type>', methods=['GET', 'POST'])
@login_required
def create_form(user_type):
    if user_type == 'advisor':
        form = AdvisorCreateForm()
    elif user_type == 'student':
        form = StudentCreateForm()
    elif user_type == 'landlord':
        form = LandlordCreateForm()
    else:
        flash('欲新增的使用者身分錯誤', 'warning')
        return redirect(url_for('create_user.user_type_form'))

    if form.validate_on_submit():
        user_id = form.id.data
        password = form.passwd.data
        name = form.name.data
        email = form.email.data
        tel = form.tel.data

        existing_user = User.query.filter_by(id=user_id).first()

        if not user_id or not name or not password or not tel or not email:
            flash('請填寫完成所有基本資料', 'danger')
            return render_template('AIMS/create_user.html', createForm=form)
        elif existing_user:
            flash('該帳號已經存在', 'danger')
            return render_template('AIMS/create_user.html', createForm=form)
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(id=user_id, name=name, passwd=hashed_password, tel=tel, email=email, type=user_type)
            db.session.add(new_user)
            db.session.commit()
            flash('使用者新增成功', 'success')

        return redirect(url_for('create_user.user_type_form'))

    return render_template('AIMS/create_user.html', createForm=form)
