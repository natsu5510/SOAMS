from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.AIMS.login_management import role_required
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, RadioField, SelectField, TextAreaField, SubmitField, TelField
from wtforms.validators import DataRequired

rental_advertisement = Blueprint('rental_advertisement', __name__)

class AdForm(FlaskForm):
    username  = StringField('username',validators=[DataRequired()])
    limit = RadioField('limit', choices=[('value','男'),('value_two','女')])
    submit = SubmitField("Submit")

@rental_advertisement.route('/')
@login_required
def index():
    form = AdForm()
    return render_template('/RIMS/rental_advertisement.html', form=form)