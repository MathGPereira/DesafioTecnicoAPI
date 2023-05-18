from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///desafio.db"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from API import routes
