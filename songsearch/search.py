import re
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
                db.words.insert_one(
                    { 'token': token, 'song': song['title'], 'sen_pos': sen_pos, 'word_pos': word_pos }
                )

def tfidf(words_match):

    return words_sort

def parse(query):
    """
    Parse query to search
    """
    db.temp.delete_many({})
    tokens = stem(query)
    
    for token in tokens:
        words_match = list(db.words.find({ 'token': token }))
        if len(words_match) != 0:
            # words_sort = tfidf(words_match)
            db.temp.insert_many(words_match)

    pipeline = [
        { '$lookup':
        {
            'from': 'temp',
            'localField': 'title',
            'foreignField': 'song',
            'as': 'match_titles',
        }},
        { '$match': 
        { 
            'match_titles': { '$ne' : [] } 
        }}
    ]
    songs = db.songs.aggregate(pipeline)
    if len(list(db.temp.find())) == 0:
        songs = [] # empty result

    return list(songs)