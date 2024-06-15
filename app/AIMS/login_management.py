from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.extensions import bcrypt, db  
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

@login_management.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('login_management.home'))
    else:
        return redirect(url_for('login_management.login'))

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

    return render_template('AIMS/login.html')

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

@login_management.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        tel = request.form.get('tel')
        email = request.form.get('email')

   
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
                new_user = User(id=user_id, name=name, passwd=hashed_password, tel=tel, email=email)
                db.session.add(new_user)
                db.session.commit()
                flash('註冊成功，請登入', 'success')
                return redirect(url_for('login_management.login'))

    return render_template('AIMS/register.html')
