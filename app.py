from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import MYSQL_USER, MYSQL_PASSWORD
from models import models

app = Flask(__name__)
app.register_blueprint(models)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/school'
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
