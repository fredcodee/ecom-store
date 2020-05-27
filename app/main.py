from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for,session
from app.models import Product, Order, Order_Item
from app import db, photos, create_app
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES
import random

main = Blueprint('main', __name__)

#add product form
class AddProduct(FlaskForm):
  name = StringField('Name')
  price = IntegerField('Price')
  stock = IntegerField('Stock')
  description = TextAreaField('Description')
  image = FileField('image', validators=[
                    FileAllowed(IMAGES, 'only images accepted.')])

#checkoutform


class Checkout(FlaskForm):
  first_name = StringField('First Name')
  last_name = StringField('Last Name')
  phone_number = StringField('Number')
  email = StringField('Email')
  address = StringField('Address')
  city = StringField('City')
  state = SelectField('State', choices=[('CA', 'California'), ('WA', 'Washington'), ('NV', 'Nevada')])
  country = SelectField('Country', choices=[('US', 'United States'), ('UK', 'United Kingdom'), ('FRA', 'France')])
  payment_type = SelectField('Payment Type', choices=[('CK', 'Check'), ('WT', 'Wire Transfer')])

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


def handle_cart():
  products = []
  grand_total = 0
  index = 0
  quantity_total = 0

  for item in session['cart']:
    product = Product.query.get(item['id'])

    quantity = int(item['quantity'])
    total = quantity * product.price
    grand_total += total

    quantity_total += quantity

    products.append({'id': product.id, 'name': product.name, 'price':  product.price,
                     'image': product.image, 'quantity': quantity, 'total': total, 'index': index})

    index += 1

  grand_total_plus_shipping = grand_total + 1000

  return(products, grand_total, grand_total_plus_shipping, quantity_total)

@main.route('/cart')
def cart():
  products, grand_total, grand_total_plus_shipping,quantity_total = handle_cart()

  return (render_template('cart.html', products=products, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total))


@main.route('/remove-from-cart/<index>')
def remove_from_cart(index):
  del session['cart'][int(index)]
  session.modified = True
  return redirect(url_for('main.cart'))


@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
  form = Checkout()

  products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()

  if form.validate_on_submit():

    order = Order()
    form.populate_obj(order)
    order.reference = ''.join([random.choice('ABCDE') for _ in range(5)])
    order.status = 'PENDING'

    for product in products:
      order_item = Order_Item(quantity=product['quantity'], product_id=product['id'])
      order.items.append(order_item)

      product = Product.query.filter_by(id=product['id']).update({'stock': Product.stock - product['quantity']})

    db.session.add(order)
    db.session.commit()

    session['cart'] = []
    session.modified = True

    return (redirect(url_for('index')))

  return (render_template('checkout.html', form=form, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total))


#Admin route
@main.route('/admin/home')
def admin():
  products = Product.query.all()
  products_in_stock = Product.query.filter(Product.stock > 0).count()
  products_out_stock = Product.query.filter(Product.stock == 0).count()

  orders = Order.query.all()

  return(render_template('admin/index.html', admin=True, products=products, products_in_stock=products_in_stock, products_out_stock=products_out_stock, orders=orders))

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
