import json
import math
import re
import time

import numpy as np
import operator

def generate_index():
    with open('./data.json', 'r') as f:
        with open('./index.txt', 'w') as f_w:
            songs = json.load(f)
            for song in songs:
                print(song)

                text = song['title'] + ' ' + song['artist'] + ' ' + song['lyrics']
                text = text.lower()
                # text = re.findall(r'\w+', text)
                print(text)

                print('=========')

                text = text.replace('\n\n', '\n').replace('\n', ' ').split(' ')
                print(text)

                # lyrics = song['lyrics'].replace('\r', '').split('\n')
                # np_lyrics = np.array([x for x in lyrics if x])

                break

def data_prep():
    data_dict = {}
    term_seq = []
    with open('./data.json', 'r') as f:
        songs = json.load(f)
        for id,song in enumerate(songs):
            # print(song)

            # text = str(song['title']) + ' ' + str(song['artist']) + ' ' + str(song['lyrics'])

            text =  str(song['lyrics'])

            text = text.lower()

            text = text.replace('\n\n', '\n').replace('\n', ' ').replace('\r', '').strip('\xa0').split(' ')
            # print(text)
            data_dict[str(id)] = text

            lyrics = song['lyrics'].replace('\r', '').split('\n')
            np_lyrics = np.array([x for x in lyrics if x])

            for sen_pos, lyric in enumerate(lyrics):
                # print(lyric)
                # break
                for word_pos, token in enumerate(lyric.split()):
                    pass

            # for term in text:
            #     tup = (term,id)
            #     term_seq.append(tup)

    # print(data_dict)
    # print(term_seq)
    return data_dict,term_seq

def new_data():
    term_seq = []
    data_dict = {}
    with open('./data.json', 'r') as f:
        songs = json.load(f)
        for id,song in enumerate(songs):
            # print(song)

            text = str(song['title']) + '\n' + str(song['artist']) + '\n' + str(song['lyrics'])
            # print(text)
            text = text.lower()
            lyrics = text.strip('\xa0').replace('\r', '').split('\n')
            # print(lyrics) # ['Got to Let Go', 'A Band of Bees', "I've got a job back in Texas",
            data_dict[id] = [a for a in lyrics if a]
            np_lyrics = np.array([x for x in lyrics if x])
            # print(np_lyrics)
            for sen_pos, lyric in enumerate(np_lyrics):
                # print(lyric)
                # break
                for word_pos, token in enumerate(lyric.split()):
                    tup = (token, id, sen_pos, word_pos)
                    term_seq.append(tup)

    # print(term_seq)
    # print(len(term_seq)) # 65308
    return data_dict, term_seq

def gen_index(term_seq):
    inv = {}
    # posting
    '''
    term_seq = [('cause', 262, 7, 0), ("there's", 262, 7, 1), ('no', 262, 7, 2),
            ('cause', 262, 7, 1), ("there's", 262, 6, 1), ('no', 262, 7, 3),
            ('i', 262, 7, 3), ('no', 666, 7, 3),('no', 666, 11, 3)]
    
        {
        'cause': {'262': [(7, 0), (7, 1)]}, 
        "there's": {'262': [(7, 1), (6, 1)]}, 
        'no': {'262': [(7, 2), (7, 3)], '666': [(7, 3), (11, 3)]}, 
        'i': {'262': [(7, 3)]}
        }
    '''

    # for tu in term_seq:
    #     if tu[0] not in inv:
    #         inv[tu[0]] = {}
    #         inv[tu[0]][str(tu[1])] = []
    #         inv[tu[0]][str(tu[1])].append((tu[2], tu[3]))
    #     else:
    #         if str(tu[1]) not in inv[tu[0]]:
    #             inv[tu[0]][str(tu[1])] = []
    #             inv[tu[0]][str(tu[1])].append((tu[2], tu[3]))
    #         else:
    #             inv[tu[0]][str(tu[1])].append((tu[2], tu[3]))

    # print(inv['i'])  # {'0': [(7, 0), (13, 0), (17, 1), (18, 1), (26, 0), (37, 1)],
    # print(len(inv['i']))
    for tu in term_seq:
        if tu[0] not in inv:
            inv[tu[0]] = {}
            # inv[tu[0]][str(tu[1])] = []
            # inv[tu[0]][str(tu[1])].append((tu[2], tu[3]))
            inv[tu[0]][str(tu[1])] = {}
            inv[tu[0]][str(tu[1])][str(tu[2])] = str(tu[3])
        else:
            if str(tu[1]) not in inv[tu[0]]:
                # inv[tu[0]][str(tu[1])] = []
                # inv[tu[0]][str(tu[1])].append((tu[2], tu[3]))
                inv[tu[0]][str(tu[1])] = {}
                inv[tu[0]][str(tu[1])][str(tu[2])] = str(tu[3])
            else:
                # inv[tu[0]][str(tu[1])].append((tu[2], tu[3]))
                inv[tu[0]][str(tu[1])][str(tu[2])] = str(tu[3])

    return inv

def gen_file(inv):
    with open('./index.txt', 'w') as f:
        for term in inv:
            # df
            f.write('token: ' + term + '\n')
            f.write('df' + ': ' + str(len(inv[term])) + '\n')
            for sid in inv[term]:
                f.write('\t' + 'song_id: ' + sid + '\n')
                f.write('\t' + 'tf: ' + str(len(inv[term][sid])) + '\n')
                f.write('\t\t' + 'pos_info (sen_pos, word_pos): '  + '\n')
                f.write('\t\t\t\t' +  str(inv[term][sid]) + '\n')
            f.write('\n')
            f.write('\n')
    print('1111111111111')


def rank_op(N, tokens, sid_list,inv):

    ranked_result = {}

    start = time.time()
    for sid in sid_list:

        score = 0

        for token in tokens:
            df = len(inv[token])
            tf = len(inv[token][sid])
            w = (1 + math.log10(tf)) * math.log10(N / df)
            score += w
        ranked_result[sid] = score
    end = time.time()
    sorted_dict = {k: v for k, v in sorted(ranked_result.items(), key=lambda x: x[1], reverse=True)}

    print(end - start)
    print(sorted_dict)

def search_op(token1, token2, inv):
    dict_1 = inv[token1]
    dict_2 = inv[token2]
    print(dict_1)

    result = []

    # r_dict = {}

    result_tup = []

    for sid_1 in dict_1:
        for sid_2 in dict_2:
            if sid_1 == sid_2:
                pos_dict_1 = dict_1[sid_1]
                pos_dict_2 = dict_2[sid_2]
                for sen_pos_1 in pos_dict_1:
                    for sen_pos_2 in pos_dict_2:
                        if sen_pos_1 == sen_pos_2:
                            result.append(sid_1)
                            # r_dict[sen_pos_1] = pos_dict_1[sen_pos_1]
                            tup = (sen_pos_1, pos_dict_1[sen_pos_1])
                            result_tup.append(tup)
    return list(set(result)),result_tup




def search_all(tokens, inv):
    temp = []
    final = []
    for i in range(len(tokens) - 2 + 1):
        result,result_tup = search_op(tokens[i:i + 2][0], tokens[i:i + 2][1], inv)

        if len(temp) == 0:
            temp = result
        else:
            temp = list(set(temp).intersection(set(result)))
    return temp



if __name__ == '__main__':
    # generate_index()

    # data_dict,term_seq = data_prep()

    data_dict, term_seq = new_data()
    # print(data_dict[0])
    '''
    ['got to let go', 'a band of bees', "i've got a job back in texas", 'cutting the grass before breakfast', 
    'cleaning the park', "i'm there til it's dark", "but i'm saving up for a lexus", "i know it's fun", 
    "but i've got to leave", 'over the sea with my family', 'just for a smile', 'to be there for a while', 
    'and the difference is true', 'i will miss you', "that's the way it is", 'as if it was planned', 
    "i've got to let go", 'if i still want your hand', 'when i return', "i'll buy you a grand", 
    'you can play the piano', 'in your own little band', 'stuff what they say', 'just thrust it away', 
    'it was all said too fast', 'we must build this to last', 'i have the blood', 'of a family man', 
    'answer to the question', 'ask as long as you can', "it's gonna take", 'a change for the world', 
    'change color and shape', 'meets every boy and girl', "that's the way it is", 'as if it was planned', 
    "i've got to let go", 'if i still want your hand']
    
    {'0': [(7, 0), (13, 0), (17, 1), (18, 1), (26, 0), (37, 1)],
    '''
    inv = gen_index(term_seq)
    # print(inv)
    #
    # print(len(data_dict[0]))  # 38 = 1 + 1 + 36

    # gen_file(inv)

    tokens = ["it's", 'been', 'a']

    start = time.time()
    # result = search_op('i', 'love', inv)
    result = search_all(tokens, inv)
    end = time.time()
    print(result)
    print(end - start)

    aaa = ['228', '245', '79', '81', '61',
           '29', '34', '36', '87', '105',
           '91', '147', '109', '243', '121',
           '111', '27', '14', '161', '139',
           '67', '100', '92', '118', '35',
           '50', '152', '248', '96', '213', '62']

    bbb = ['67', '243', '14', '147', '118',
           '61', '111', '139', '96', '62',
           '36', '87', '92', '152', '29',
           '105', '213', '100', '50', '81',
           '248', '34', '109', '35', '161',
           '27', '228', '121', '79', '245', '91']

    print(operator.eq(set(aaa), set(bbb)))

    # ['87', '79', '67', '111', '228', '91', '213', '34', '27', '36', '61', '139', '105', '50', '29', '118', '92']
    print(data_dict[100])

    print(len(data_dict))

    N = len(data_dict)

    rank_op(N,tokens,result, inv)







