from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for,session
from app.models import Product, Order
from app import db, photos, create_app
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES

main = Blueprint('main', __name__)

#add product form
class AddProduct(FlaskForm):
  name = StringField('Name')
  price = IntegerField('Price')
  stock = IntegerField('Stock')
  description = TextAreaField('Description')
  image = FileField('image', validators=[
                    FileAllowed(IMAGES, 'only images accepted.')])

#cart
class AddToCart(FlaskForm):
  quantity = IntegerField('Quantity')
  id = HiddenField('ID')

#routes
@main.route("/")
def home():
  products = Product.query.all()

  return(render_template('index.html', products=products))

#view product page
@main.route('/product/<idd>')
def product(idd):
  product=Product.query.get(int(idd))
  form = AddToCart()

  return (render_template('view-product.html', product=product, form=form))

#carts
@main.route('/quick-add/<id>')
def quick_add(id):
  if 'cart' not in session:
    session['cart'] = []

  session['cart'].append({'id': id, 'quantity': 1})
  session.modified = True

  return(redirect(url_for('main.home')))

@main.route('/add-to-cart', methods=['POST'])
def add_to_cart():
  if 'cart' not in session:
    session['cart'] = []

  form = AddToCart()

  if form.validate_on_submit():

    session['cart'].append({'id': form.id.data, 'quantity': form.quantity.data})
    session.modified = True

  return (redirect(url_for('main.home')))

@main.route('/cart/<id>')
def cart(id):
  print(session['cart'])
  return(render_template('cart.html'))


@main.route('/checkout')
def checkout():
    return (render_template('checkout.html'))


#Admin route
@main.route('/admin/home')
def admin():
  products = Product.query.all()
  products_in_stock = Product.query.filter(Product.stock > 0).count()
  products_out_stock = Product.query.filter(Product.stock == 0).count()

  return(render_template('admin/index.html', admin=True, products=products, products_in_stock=products_in_stock, products_out_stock=products_out_stock))

#add products to inventory
@main.route('/admin/add', methods=["GET","POST"])
def add():
  form = AddProduct()
  if form.validate_on_submit():
    new_product = Product(name=form.name.data,
                          stock=form.stock.data, price=form.price.data, description=form.description.data, image=photos.save(form.image.data))
    db.session.add(new_product)
    db.session.commit()
    return(redirect(url_for('main.admin')))

  return(render_template('admin/add-product.html', admin=True, form= form))

#delete product inventory
@main.route('/admin/delete/<id>')
def delete(id):
  get_p = Product.query.get(int(id))
  db.session.delete(get_p)
  db.session.commit()
  return(redirect(url_for('main.admin')))
