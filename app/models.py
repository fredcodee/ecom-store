from datetime import datetime
from app import db


class Product(db.Model):
  __tablename__ = 'product'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  stock= db.Column(db.Integer)
  price = db.Column(db.Integer)
  description = db.Column(db.String)
  pic = db.Column(db.LargeBinary(), nullable=False)
  orders = db.relationship('Order', backref='activity', lazy=True)

  def __repr__(self):
    return('<Product- %r>' % (self.name))

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order_num = db.Column(db.String, nullable=False)
  name = db.Column(db.String(300), nullable=False)
  shipping_address = db.Column(db.String)
  country = db.Column(db.String)
  quantity = db.Column(db.Integer)
  method = db.Column(db.String)
  payment_option = db.Column(db.String)
  product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
  checklist = db.Column(db.Boolean)

