import os

from flask import Flask
from flask_pymongo import PyMongo

from songsearch import search

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# app.config["MONGO_URI"] = "mongodb+srv://ttds:VqLiQ1qYShEoqolv@ttds.s6ptp.mongodb.net/songsearch?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/songsearch"

db = PyMongo(app).db

from songsearch import views, errors, commands, search