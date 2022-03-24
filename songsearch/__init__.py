import os, time
import pickle

from tqdm import tqdm
from collections import defaultdict

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config["MONGO_URI"] = "mongodb://localhost:27017/songsearch"

db = PyMongo(app).db

db.songs.create_index('title')

N = db.songs.count_documents({})

start_time = time.time()
print(f'Lyrics length load start.')
with open('./lyric_len.pkl', 'rb') as f:
    lyric_len = pickle.load(f)
loadtime = round(time.time() - start_time + 0.000005, 5)
LEN_A = lyric_len['<lyrics_len>']
print(f'Lyrics length load done with {loadtime}s.')

start_time = time.time()
print(f'Inv load start.')
with open('./index.pkl', 'rb') as f:
    inv = pickle.load(f)
loadtime = round(time.time() - start_time + 0.000005, 5)
print(f'Inv load done with {loadtime}s.')

# lyric_len = {}

# inv = {}

from songsearch import views, errors, commands, search