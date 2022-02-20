import os, certifi

from flask import Flask
from flask_pymongo import PyMongo

# TLS connection certifi
ca = certifi.where()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config["MONGO_URI"] = "mongodb+srv://ttds:VqLiQ1qYShEoqolv@ttds.s6ptp.mongodb.net/songsearch?retryWrites=true&w=majority"

db = PyMongo(app, tlsCAFile=ca).db

from songsearch import views, errors, commands, search