from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for
from app.models import Product, Order
from app import db, photos
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES

main = Blueprint('main', __name__)

#add product form
class AddProduct(FlaskForm):
  name = StringField('Name')
  price = IntegerField('Price')
  stock = IntegerField('Price')
  description = TextAreaField('Description')
  image = FileField('image', validators=[
                    FileAllowed(IMAGES, 'only images accepted.')])

#routes
@main.route("/")
def home():
  products = Product.query.all()

  return(render_template('index.html', products=products))


@main.route('/product/<idd>')
def product(idd):
  pass


@main.route('/cart')
def cart():
  pass


@main.route('/admin/home')
def admin():
  products = Product.query.all()
  products_in_stock = Product.query.filter(Product.stock > 0).count()
  products_out_stock = Product.query.filter(Product.stock == 0).count()

  return(render_template('admin/index.html', admin=True, products=products, products_in_stock=products_in_stock, products_out_stock=products_out_stock))


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


from flask import send_from_directory


"""@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
"""