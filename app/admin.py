from flask import Blueprint
from app import db,admin
from flask_admin.contrib.sqla import ModelView
from app.models import Products, Order

bp = Blueprint('admin_bp', __name__)

admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Order, db.session))
