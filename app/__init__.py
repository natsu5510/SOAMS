import datetime
from flask import Flask
from app.extensions import db, login_manager, bcrypt
from config import MYSQL_USER, MYSQL_PASSWORD, SECRET_KEY


def create_app():
    app = Flask(__name__)

    from app.AIMS.login_management import login_management
    app.register_blueprint(login_management)
    from app.AIMS.update_user_information import update_user_information
    app.register_blueprint(update_user_information)
    from app.AIMS.search_user_information import search_user_information
    app.register_blueprint(search_user_information)
    from app.AIMS.create_user_information import create_user_information
    app.register_blueprint(create_user_information)
    from app.AIVS.accommodation_management import accommodation_management
    app.register_blueprint(accommodation_management, url_prefix='/AIVS')
    from app.RIMS.rental_advertisement import rental_advertisement
    app.register_blueprint(rental_advertisement, url_prefix='/rental_advertisement')

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
