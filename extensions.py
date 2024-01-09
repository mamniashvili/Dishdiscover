from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "bc5{VPK"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/files'

database = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
