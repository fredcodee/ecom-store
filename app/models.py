from datetime import datetime
from app import db


class Product(db.Model):
  __tablename__ = 'product'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  stock= db.Column(db.Integer)
  price = db.Column(db.Integer)
  description = db.Column(db.String(500))
  image = db.Column(db.String(500))
  orders = db.relationship('Order_Item', backref='product', lazy=True)

  def __repr__(self):
    return('<Product- %r>' % (self.name))


class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  reference = db.Column(db.String(5))
  first_name = db.Column(db.String(20))
  last_name = db.Column(db.String(20))
  phone_number = db.Column(db.Integer)
  email = db.Column(db.String(50))
  address = db.Column(db.String(100))
  city = db.Column(db.String(100))
  state = db.Column(db.String(20))
  country = db.Column(db.String(20))
  status = db.Column(db.String(10))
  payment_type = db.Column(db.String(10))
  items = db.relationship('Order_Item', backref='order', lazy=True)

  def order_total(self):
    return db.session.query(db.func.sum(Order_Item.quantity * Product.price)).join(Product).filter(Order_Item.order_id == self.id).scalar() + 1000

  def quantity_total(self):
    return db.session.query(db.func.sum(Order_Item.quantity)).filter(Order_Item.order_id == self.id).scalar()


class Order_Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
  quantity = db.Column(db.Integer)
