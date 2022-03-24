import json, math, re, time
import numpy as np
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from tqdm import tqdm

from songsearch import db, N, LEN_A, inv, lyric_len

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

def new_data(path):
    term_seq = []
    data_dict = {}

    with open(path, 'r+', encoding='utf-8') as f:
        songs = json.load(f)
        for song in tqdm(songs):
            # text = str(song['title']) + '\n' + str(song['artist']) + '\n' + str(song['lyrics'])
            text = song['lyrics']
            lyrics = text.lower().strip('\xa0').replace('\r', '').split('\n')
            data_dict[song['title']] = [a for a in lyrics if a]
            
            for sen_pos, lyric in enumerate(np.array(data_dict[song['title']])):
                for word_pos, token in enumerate(stem(lyric)):
                    tup = (token, song['title'], sen_pos, word_pos)
                    term_seq.append(tup)

    return data_dict, term_seq

def gen_index(term_seq):
    # {'cause': {'262': {7: [0,1]} } }

    inv = defaultdict(dict)

    for term in tqdm(term_seq, total=db.words.count_documents({})):
        (idx, token, title, sen, word) = term.values()
        inv[token].setdefault(title, defaultdict(list))[str(sen)].append(word)

    return inv

def rank_tfidf(N, tokens, result, inv):
    ranked_result = {}

    for title in result:
        score = 0
        for token in tokens:
            df = len(inv[token])
            tf = len(inv[token][title])
            w = (1 + math.log10(tf)) * math.log10(N / df)
            score += w
        ranked_result[title] = score

    sorted_dict = {k: v for k, v in sorted(result.items(), key=lambda x: ranked_result[x[0]], reverse=True)}

    return sorted_dict

def rank_bm25(N, tokens, result, inv):
    ranked_result = {}
    k, b = 1.2, 0.75

    for title in result:
        score = 0
        for token in tokens:
            df = len(inv[token])
            idf = math.log10(N / df)
            tf = len(inv[token][title])
            bm25 = idf * ((k+1) * tf) / (k * (1-b+b*lyric_len[title]/LEN_A) + tf)
            score += bm25
        ranked_result[title] = score

    sorted_dict = {k: v for k, v in sorted(result.items(), key=lambda x: ranked_result[x[0]], reverse=True)}

    return sorted_dict

def search_pair_song(dict_1, dict_2):
    result = {}
    
    for title in dict_1:
        if title in dict_2:
            if title not in result:
                result[title] = {'100': set([])}
            for sen_pos in dict_1[title]:
                if sen_pos not in result[title]:
                    result[title][sen_pos] = set(dict_1[title][sen_pos])
                            
    return result

def search_pair_sen(dict_1, dict_2):
    result = {}
    
    for title in dict_1:
        if title in dict_2:
            for sen_pos in dict_1[title]:
                if sen_pos in dict_2[title]:
                    if title not in result:
                        result[title] = {}
                    if sen_pos not in result[title]:
                        result[title][sen_pos] = set()
                    result[title][sen_pos] = result[title][sen_pos] | set(dict_1[title][sen_pos]) | set(dict_2[title][sen_pos])
                            
    return result

def search(tokens, inv, type):
    t = []

    if len(tokens) == 1:
        return inv[tokens[0]]

    for i in range(len(tokens) - 1):
        if type == 'key':
            r = search_pair_song(inv[tokens[i]], inv[tokens[i+1]])
        elif type == 'lyric':
            r = search_pair_sen(inv[tokens[i]], inv[tokens[i+1]])
        if len(t) == 0:
            t = r
        else:
            t = {k:{s:set(t[k][s] | r[k][s]) for s in t[k].keys() & r[k].keys()} for k in t.keys() & r.keys()}
    return t

def parse(query, type):

    tokens = stem(query)

    # Query just indeludes stop words
    if tokens == []:
        return [], [], 0.00000
    # No matched songs
    for token in tokens:
        if token not in inv:
            return [], [], 0.00000
            
    # result = search(tokens, inv)
    # sorted_dict = rank(N, tokens, result, inv)
    # songs = db.songs.find({ 'title': {'$in': list(sorted_dict.keys()) } })

    search_time = time.time()

    start_time = time.time()
    result = search(tokens, inv, type)
    stime = round(time.time() - start_time + 0.000005, 5)
    print(f'Search done with {stime}s.')

    start_time = time.time()
    if type == 'key':
        sorted_dict = rank_tfidf(N, tokens, result, inv)
    elif type == 'lyric':
        sorted_dict = rank_bm25(N, tokens, result, inv)
    sotime = round(time.time() - start_time + 0.000005, 5)
    print(f'Rank done with {sotime}s.')

    start_time = time.time()

    # songs = []
    # for title in list(sorted_dict.keys()):
    #     songs.append(db.songs.find_one({ 'title': title }))

    titles =list(sorted_dict.keys())
    songs = db.songs.find({ 'title': {'$in': titles } }, { '_id': 0 }).limit(3000)

    sort_dict = {d['title']: d for d in songs}
    valid_titles = sort_dict.keys()
    songs = [sort_dict[i] for i in titles if i in valid_titles]

    # print(titles)
    ftime = round(time.time() - start_time + 0.000005, 5)
    print(f'Find done with {ftime}s.')

    searched_time = round(time.time() - search_time + 0.000005, 5)

    return songs, sorted_dict, searched_time








