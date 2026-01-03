from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth
    from app.routes.employee import employee
    from app.routes.admin import admin
    from app.routes.attendance import attendance
    from app.routes.leave import leave
    from app.routes.payroll import payroll
    from app.routes.reports import reports
    
    app.register_blueprint(auth)
    app.register_blueprint(employee)
    app.register_blueprint(admin)
    app.register_blueprint(attendance)
    app.register_blueprint(leave)
    app.register_blueprint(payroll)
    app.register_blueprint(reports)
    
    return app
