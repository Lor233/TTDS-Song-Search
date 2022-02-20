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
                token_db = list(db.inverted_index.find({ 'token': token }))
                song_exist = False
                if len(token_db) != 0:
                    songs = token_db[0]['songs']
                    for i, in_song in enumerate(songs):
                        if in_song['song_id'] == song['_id']:
                            songs[i]['song_count'] += 1
                            songs[i]['word'].append({ 'sen_pos': sen_pos, 'word_pos': word_pos })
                            song_exist = True
                        if song_exist==False:
                            songs.append({ 'song_id': song['_id'], 'song_count': 1, 'word':
                                            [{ 'sen_pos': sen_pos, 'word_pos': word_pos
                                            }]
                                        })
                if len(token_db) == 0:
                    db.inverted_index.insert_one(
                        { 'token': token, 'count': 1, 'songs':
                            [{ 'song_id': song['_id'], 'song_count': 1, 'word':
                                [{ 'sen_pos': sen_pos, 'word_pos': word_pos
                                }]
                            }]
                        }
                    )
                else:
                    db.inverted_index.update_one({ '_id': token_db[0]['_id'] }, { '$set': 
                        { 'count': token_db[0]['count']+1,  'songs': songs }
                    })