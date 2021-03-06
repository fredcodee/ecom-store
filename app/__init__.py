from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES

photos = UploadSet("photos",IMAGES)

db = SQLAlchemy()
migrate = Migrate()

def create_app():
  app = Flask(__name__)

  app.config['UPLOADED_PHOTOS_DEST']='app/static/productimages'
  app.config['SECRET_KEY'] = '2020plsbebetter'
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://awmtkzvxewzxkn:28bce3779603ee267b22be337ea5b5372079d4d6a858f2c6e851368dd8f5a6eb@ec2-52-202-22-140.compute-1.amazonaws.com:5432/ddqtm244hd7q32"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  from app.models import Product, Order
  migrate.init_app(app, db)
  configure_uploads(app, photos)

  # blueprint for non-auth parts of app
  from app.main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return(app)
