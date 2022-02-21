import re, time
import numpy as np
from nltk.stem import PorterStemmer
from tqdm import tqdm

from songsearch import db

def stem(text):
    """
    Preprocess text with stem and lower case converting
    :param  text        : text need to preprocess
    :return tokens      : preprocessed text
    """
    # Load words including numbers and letters with regular expression
    tokens = re.findall("[\w]+", text)
    # Covert words to lower case, stem them with Porter stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(x.lower()) for x in tokens]
    return tokens

def invertedIndex():
    """
    Generate inverted index based on DB data
    """
    for song in tqdm(db.songs.find({}), total=db.songs.count_documents({})):
        lyrics = song['lyrics'].replace("\r", "").split('\n')
        lyrics = np.array([x for x in lyrics if x])
        for sen_pos, lyric in enumerate(lyrics):
            for word_pos, token in enumerate(stem(lyric)):
                token_db = list(db.inverted_index.find({ 'token': token }))
                db.words.insert_one(
                    { 'token': token, 'song_id': song['_id'], 'sen_pos': sen_pos, 'word_pos': word_pos }
                )
                if len(token_db) == 0:
                    db.inverted_index.insert_one(
                        { 'token': token, 'song_id': song['_id'], 'count': 1 }
                    )
                else:
                    db.inverted_index.update_one(
                        { '_id': token_db[0]['_id'], 'song_id': song['_id'] }, 
                        { '$set': { 'count': token_db[0]['count'] + 1 } }
                    )