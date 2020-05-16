from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify, url_for, abort
from app.models import Product,Order
from app import db, photos
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

#routes
@main.route("/", methods=['POST', 'GET'])
def home():
  pass


@main.route('/admin')
def admin():
  return(render_template('admin/index.html', admin = True))


@main.route('/admin/add', methods=["GET","POST"])
def add():
  form = AddProduct()
  if form.validate_on_submit():
    image_url = photos.url(photos.save(form.image.data))
    new_product = Product(name=form.name.data,
                          stock=form.stock.data, price=form.price.data,description=form.description.data,image=image_url )
    db.session.add(new_product)
    db.session.commit()
    return(redirect(url_for('main.admin')))

  return(render_template('admin/add-product.html', admin=True, form= form))
