from flask import Flask, Blueprint, redirect, render_template, request, flash, jsonify, url_for, abort
#from app.models import User, Favourites
from app import db

main = Blueprint('main', __name__)


@main.route("/", methods=['POST', 'GET'])
def home():
  pass
