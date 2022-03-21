import re, json, time
from turtle import pos
import numpy as np
from tqdm import tqdm
from math import log10

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from songsearch import db

N = len(list(db.songs.find()))

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
    stop_words = set(stopwords.words('english')) 
    tokens = [stemmer.stem(x.lower()) for x in tokens if x.lower() not in stop_words]
    return tokens

def invertedIndex():
    """
    Generate inverted index based on DB data
    """

    inv = []

    for song in tqdm(db.songs.find({}), total=db.songs.count_documents({})):
        lyrics = song['lyrics'].replace("\r", "").split('\n')
        lyrics = np.array([x for x in lyrics if x])
        for sen_pos, lyric in enumerate(lyrics):
            for word_pos, token in enumerate(stem(lyric)):
                inv.append(
                    { 'token': token, 'song': song['title'], 'sen_pos': sen_pos, 'word_pos': word_pos }
                )

    path = 'term_seq.json'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('[\n')
        for i, s in tqdm(enumerate(inv), total=len(inv)):
            json.dump(s, f, ensure_ascii=False)
            if i != len(inv)-1:
                f.write(',\n')
            else:
                f.write('\n')
        f.write(']')

    path = 'term_seq.json'
    with open(path, 'r+', encoding='utf-8') as f:
        inv = json.load(f)

    start_time = time.time()

    db.words.insert_many(inv)

    print(round(time.time() - start_time, 5))


def tfidf(tokens):

    db.temp.create_index('token')

    scores = dict.fromkeys(db.temp.find({}, { 'song': 1 }).distinct('song'), 0)
    # Construct dictionary of doc_or with TFIDF scores
    for token in tokens:
        df = len(list(db.temp.find({ 'token': token }).distinct('song')))
        for word in db.temp.find({ 'token': token }):
            tf = db.temp.count_documents({ 'token': token, 'song': word['song'] })
            scores[word['song']] += (1+log10(tf))*log10(N/df)

    sort_scores = sorted(scores.items(), key=lambda item:item[1], reverse=True)
    # print(sort_scores)
    return sort_scores

def parse(query):
    """
    Parse query to search
    """
    db.temp.delete_many({})
    tokens = stem(query)
    
    for token in tokens:
        words_match = list(db.words.find({ 'token': token }))
        if len(words_match) != 0:
            db.temp.insert_many(words_match)

    db.temp.create_index('song')

    if len(list(db.temp.find())) != 0:
        sort = tfidf(tokens)

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
        songs = sorted(list(songs), key=lambda x:dict(sort)[x['title']], reverse=True)
    else:
        songs = [] # empty result

    return list(songs)