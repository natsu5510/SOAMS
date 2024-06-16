from flask import Blueprint, request, flash, redirect, url_for, render_template
from wtforms.fields.simple import SubmitField, StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Email

from app import bcrypt, db
from app.AIMS.user_forms import LandlordForm
from app.models import Landlord, User

land_lord_register = Blueprint('land_lord_register', __name__)


class LandlordRegisterForm(LandlordForm):
    id = StringField('帳號(使用者ID)', validators=[DataRequired()])
    passwd = PasswordField('密碼設置', validators=[DataRequired()])
    confirm_passwd = PasswordField('確認密碼', validators=[DataRequired()])
    type = HiddenField('使用者身分', default='landlord', validators=[DataRequired()])
    submit = SubmitField('註冊完成')


@land_lord_register.route('/register', methods=['GET', 'POST'])
def register():
    form = LandlordRegisterForm()

    if form.validate_on_submit():
        user_id = form.id.data
        password = form.passwd.data
        confirm_password = form.confirm_passwd.data
        name = form.name.data
        email = form.email.data
        tel = form.tel.data

        if password != confirm_password:
            flash('您輸入的密碼不一致，請重新輸入', 'danger')
        elif not user_id or not name or not password or not confirm_password or not tel or not email:
            flash('請填寫完成所有基本資料', 'danger')
        else:
            existing_user = User.query.filter_by(id=user_id).first()
            if existing_user:
                flash('該帳號已經被註冊過', 'danger')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = Landlord(id=user_id, name=name, passwd=hashed_password, tel=tel, email=email)
                db.session.add(new_user)
                db.session.commit()
                flash('註冊成功，請登入', 'success')
                return redirect(url_for('login_management.login'))

    return render_template('AIMS/land_lord_register.html', registerForm=form)
