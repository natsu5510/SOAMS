from flask import Flask, flash, redirect, url_for
from config import MYSQL_USER, MYSQL_PASSWORD, SECRET_KEY
from app.extensions import db, login_manager, bcrypt
from functools import wraps
import datetime


def create_app():

    app = Flask(__name__)

    from app.AIMS.login_management import login_management
    app.register_blueprint(login_management, url_prefix='/AIMS')
    from app.AIVS.accommodation_management import accommodation_management
    app.register_blueprint(accommodation_management, url_prefix='/AIVS')
    from app.RIMS.rental_advertisement import rental_advertisement
    app.register_blueprint(rental_advertisement, url_prefix='/RIMS')

    app.secret_key = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/SOAMS'
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login_management.login'
    login_manager.login_message = '請登入'
    login_manager.login_message_category = 'warning'
    login_manager.session_protection = 'strong'

    with app.app_context():
        db.create_all()  # 確保資料庫被創建

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(user_id)