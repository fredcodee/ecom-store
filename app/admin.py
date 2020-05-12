from app import db,admin
from flask_admin.contrib.sqla import ModelView
from app.models import Products, Order

admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Order, db.session))
