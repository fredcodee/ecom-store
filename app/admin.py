from flask import Blueprint
from app import db,admin
from flask_admin.contrib.sqla import ModelView
from app.models import Product, Order


bp = Blueprint('admin_bp', __name__)

#table views
class ProductView(ModelView):
  column_display_pk = True
  can_upload = True

admin.add_view(ProductView(Product, db.session))
admin.add_view(ModelView(Order, db.session))