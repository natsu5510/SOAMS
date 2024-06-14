from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

from app.models import User

search_user_information = Blueprint('search_user_information', __name__)


class UserSearchForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('查詢')


@search_user_information.route('/search_user_information', methods=['GET', 'POST'])
@login_required
def search_form():
    form = UserSearchForm()
    if form.validate_on_submit():
        user_id = form.id.data
        # user = User.query.filter_by(id=user_id).first()
        # if user is None:
        #     flash('查無使用者', 'warning')
        #     return render_template('AIMS/search_user_information.html', searchForm=form)
        return redirect(url_for('update_user_information.update_form', user_id=user_id))

    return render_template('AIMS/search_user_information.html', searchForm=form)
