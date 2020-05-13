from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(template_mode='bootstrap3')

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = '2020plsbebetter'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cre.db'
  #heroku db
  #postgres://awmtkzvxewzxkn:28bce3779603ee267b22be337ea5b5372079d4d6a858f2c6e851368dd8f5a6eb@ec2-52-202-22-140.compute-1.amazonaws.com:5432/ddqtm244hd7q32

  db.init_app(app)
  from app.models import Products, Order
  migrate.init_app(app, db)
  admin.init_app(app)

  # blueprint for non-auth parts of app
  from app.main import main as main_blueprint
  app.register_blueprint(main_blueprint)
  
  #admin panel
  from app.admin import bp as admin_bp
  app.register_blueprint(admin_bp)

  return(app)
