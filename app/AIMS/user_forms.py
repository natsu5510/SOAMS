from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    id = StringField('使用者ID', validators=[DataRequired()])
    passwd = PasswordField('密碼', validators=[DataRequired()])
    name = StringField('名稱', validators=[DataRequired()])
    email = StringField('電子郵件', validators=[DataRequired(), Email('請輸入正確的電子郵件地址')])
    tel = StringField('電話', validators=[DataRequired()])
    submit = SubmitField('確認')


class AdministratorForm(UserForm):
    pass


class AdvisorForm(UserForm):
    dept = StringField('系所', validators=[DataRequired()])
    rank = StringField('職級', validators=[DataRequired()])
    office_addr = StringField('辦公室位址', validators=[DataRequired()])
    office_tel = StringField('辦公室電話', validators=[DataRequired()])


class StudentForm(UserForm):
    dept = StringField('系所', validators=[DataRequired()])
    enroll_year = IntegerField('入學年分', validators=[DataRequired()])
    sex = SelectField('性別', choices=[('1', '男'), ('0', '女')], validators=[DataRequired()])
    home_addr = StringField('家中地址')
    home_tel = StringField('家裡電話')
    contact_name = StringField('聯絡人姓名')
    contact_tel = StringField('聯絡人電話')


class LandlordForm(UserForm):
    pass