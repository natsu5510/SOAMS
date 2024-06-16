from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

search_user_information = Blueprint('search_user_information', __name__)


class UserSearchForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('查詢')


@search_user_information.route('/update/search_user_information', methods=['GET', 'POST'])
@login_required
def update_search_form():
    form = UserSearchForm()
    if form.validate_on_submit():
        user_id = form.id.data
        return redirect(url_for('update_user_information.update_form', user_id=user_id))

    return render_template('AIMS/search_user_information.html', searchForm=form, operation='update')


@search_user_information.route('/delete/search_user_information', methods=['GET', 'POST'])
@login_required
def delete_search_form():
    form = UserSearchForm()
    if form.validate_on_submit():
        user_id = form.id.data
        return redirect(url_for('delete_user.delete_form', user_id=user_id))

    return render_template('AIMS/search_user_information.html', searchForm=form, operation='delete')