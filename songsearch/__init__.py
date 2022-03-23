import os, time
import pickle

from tqdm import tqdm
from collections import defaultdict

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# app.config["MONGO_URI"] = "mongodb+srv://ttds:VqLiQ1qYShEoqolv@ttds.s6ptp.mongodb.net/songsearch?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/songsearch"

db = PyMongo(app).db

N = db.songs.count_documents({})

start_time = time.time()
print(f'Inv load start.')
with open('./index.pkl', 'rb') as f:
    inv = pickle.load(f)
loadtime = round(time.time() - start_time + 0.000005, 5)
print(f'Inv load done with {loadtime}s.')

# inv = {}

from songsearch import views, errors, commands, search