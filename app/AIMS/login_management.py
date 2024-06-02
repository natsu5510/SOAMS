from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.extensions import bcrypt

login_management = Blueprint('login_management', __name__)

# 自定義裝飾器，檢查使用者角色
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_anonymous or not current_user.is_authenticated:
                flash('請登入', 'warning')
                return redirect(url_for('login_management.login'))
            if current_user.type != role:
                logout_user()
                flash('請勿嘗試非法動作，為確保網站安全，已將您登出', 'danger')
                return redirect(url_for('login_management.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_management.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.query.filter_by(id=user_id).first()
        
        if user and bcrypt.check_password_hash(user.passwd, password):
            login_user(user)
            return redirect(url_for('login_management.home'))
        else:
            flash('帳號或密碼錯誤', 'danger')
    
    return render_template('/AIMS/login.html')

@login_management.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出', 'success')
    return redirect(url_for('login_management.login'))

@login_management.route('/home')
@login_required
def home():
    return render_template('home.html')