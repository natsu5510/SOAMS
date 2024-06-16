from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import DataRequired

from app import bcrypt, db
from app.AIMS.user_forms import AdvisorForm, StudentForm, LandlordForm, AdministratorForm
from app.models import User, Administrator, Advisor, Student, Landlord

create_user = Blueprint('create_user', __name__)


class UserTypeForm(FlaskForm):
    user_type = SelectField('使用者身分',
                            choices=[('', '請選擇'), ('administrator', '管理員'), ('advisor', '導師'),
                                     ('student', '學生'), ('landlord', '房東')],
                            validators=[DataRequired()], default='')
    submit = SubmitField('確認')


class AdministratorCreateForm(AdministratorForm):
    type = HiddenField('使用者身分', default='administrator', validators=[DataRequired(message='* 此欄位不可為空')])
    submit = SubmitField('新增')


class AdvisorCreateForm(AdvisorForm):
    type = HiddenField('使用者身分', default='advisor', validators=[DataRequired(message='* 此欄位不可為空')])
    submit = SubmitField('新增')


class StudentCreateForm(StudentForm):
    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)
        default_advisor = [('', '請選擇')]
        existing_advisors = [(advisor.id, advisor.name) for advisor in Advisor.query.all()]
        all_advisors = default_advisor + existing_advisors
        self.advisor_id.choices = all_advisors

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
    print(user_type)
    if user_type == 'administrator':
        form = AdministratorCreateForm()
    elif user_type == 'advisor':
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
        existing_user = User.query.filter_by(id=user_id).first()

        if existing_user:
            flash('該帳號已經存在', 'danger')
        else:
            if user_type == 'administrator':
                hashed_passwd = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
                new_user = Administrator(id=form.id.data,
                                         passwd=hashed_passwd,
                                         name=form.name.data,
                                         tel=form.tel.data,
                                         email=form.email.data)
            elif user_type == 'advisor':
                hashed_passwd = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
                new_user = Advisor(id=form.id.data,
                                   passwd=hashed_passwd,
                                   name=form.name.data,
                                   tel=form.tel.data,
                                   dept=form.dept.data,
                                   rank=form.rank.data,
                                   office_addr=form.office_addr.data,
                                   office_tel=form.office_tel.data)
            elif user_type == 'student':
                hashed_passwd = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
                new_user = Student(id=form.id.data,
                                   passwd=hashed_passwd,
                                   name=form.name.data,
                                   tel=form.tel.data,
                                   email=form.email.data,
                                   dept=form.dept.data,
                                   enroll_year=form.enroll_year.data,
                                   sex=form.sex.data,
                                   home_addr=form.home_addr.data,
                                   home_tel=form.home_tel.data,
                                   contact_name=form.contact_name.data,
                                   contact_tel=form.contact_tel.data,
                                   advisor_id=form.advisor_id.data)
            elif user_type == 'landlord':
                hashed_passwd = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
                new_user = Landlord(id=form.id.data,
                                    passwd=hashed_passwd,
                                    name=form.name.data,
                                    tel=form.tel.data,
                                    email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash('使用者已成功新增', 'success')
            return redirect(url_for('create_user.user_type_form'))

        return redirect(url_for('create_user.user_type_form'))

    return render_template('AIMS/create_user.html', createForm=form)
