from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'employees.signin'
login_manager.login_message_category = 'info'


from eds.employees.routes import employees
from eds.main.routes import main
from eds.admin.routes import admin
from eds.errors.handlers import errors

app.register_blueprint(employees)
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(errors)
