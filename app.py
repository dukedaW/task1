from flask import Flask, render_template, jsonify, Blueprint, redirect, url_for, request
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, DateField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task1.db"
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)
