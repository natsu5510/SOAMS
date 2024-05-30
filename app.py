from flask import Flask
from config import MYSQL_USER, MYSQL_PASSWORD
from extensions import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/SOAMS'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 確保資料庫被創建
    app.debug = True
    app.run()
