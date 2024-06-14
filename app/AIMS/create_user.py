from flask import Blueprint, render_template
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField, HiddenField
from wtforms.validators import DataRequired

from app.AIMS.user_forms import AdvisorForm, StudentForm, LandlordForm

create_user = Blueprint('create_user', __name__)


class UserTypeForm(FlaskForm):
    user_type = SelectField('使用者身分',
                            choices=[('', '請選擇'), ('advisor', '導師'), ('student', '學生'), ('landlord', '房東')],
                            validators=[DataRequired()], default='')
    submit = SubmitField('確認')


class AdvisorCreateForm(AdvisorForm):
    type = HiddenField('使用者身分', default='advisor')
    submit = SubmitField('新增')


class StudentCreateForm(StudentForm):
    type = HiddenField('使用者身分', default='student')
    submit = SubmitField('新增')


class LandlordCreateForm(LandlordForm):
    type = HiddenField('使用者身分', default='landlord')
    submit = SubmitField('新增')


@create_user.route('/create_user_type', methods=['GET', 'POST'])
@login_required
def user_type_form():
    form = UserTypeForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        if user_type == 'advisor':
            return render_template('AIMS/create_user.html', createForm=AdvisorCreateForm())
        elif user_type == 'student':
            return render_template('AIMS/create_user.html', createForm=StudentCreateForm())
        elif user_type == 'landlord':
            return render_template('AIMS/create_user.html', createForm=LandlordCreateForm())

    return render_template('AIMS/create_user_type.html', typeForm=form)


@create_user.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_form():
    return render_template('AIMS/create_user.html', createForm=None)
