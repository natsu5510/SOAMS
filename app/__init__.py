from flask import Flask
from config import MYSQL_USER, MYSQL_PASSWORD
from app.extensions import db

from app.AIMS.aims import aims
from app.AIVS.aivs import aivs
from app.RIMS.rims import rims

def create_app():

    app = Flask(__name__)

    app.register_blueprint(aims, url_prefix='/AIMS')
    app.register_blueprint(aivs, url_prefix='/AIVS')
    app.register_blueprint(rims, url_prefix='/RIMS')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/SOAMS'
    db.init_app(app)

    with app.app_context():
        db.create_all()  # 確保資料庫被創建

    # app.add_url_rule('/', '/', hello_world)

    return app