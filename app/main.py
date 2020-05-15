from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify, url_for, abort
#from app.models import User, Favourites
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES

main = Blueprint('main', __name__)

#product form
class AddProduct(FlaskForm):
  name = StringField('Name')
  price = IntegerField('Price')
  stock = IntegerField('Price')
  description = TextAreaField('Description')
  image = FileField('image', validators=[
                    FileAllowed(IMAGES, 'only images accepted.')])

@main.route("/", methods=['POST', 'GET'])
def home():
  pass

@main.route('/admin/add')
def add():
  form = AddProduct()
  return(render_template('admin/add-product.html', admin=True, form= form))
