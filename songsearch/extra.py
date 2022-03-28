import pickle
import string
import time

with open('./songsearch/models/voc_dict.pkl', 'rb') as f:
    voc_dict = pickle.load(f)

with open('./songsearch/models/2_gram.pkl', 'rb') as f:
    _2gram_model = pickle.load(f)

def _is_known(token):
    return token in voc_dict

def _tokens_1_edit_away(token):
    chars = string.ascii_lowercase + "'"
    splits = [(token[:i], token[i:]) for i in range(len(token) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in chars]
    inserts = [L + c + R for L, R in splits for c in chars]
    return set(deletes + transposes + replaces + inserts)

def _tokens_2_edits_away(token):
    res = set()
    for e1 in _tokens_1_edit_away(token):
        res |= _tokens_1_edit_away(e1)
    return res

def _get_candidates(token):
    candidates_1_edit = _tokens_1_edit_away(token) & voc_dict.keys()
    if candidates_1_edit:
        return candidates_1_edit
    else:
        return _tokens_2_edits_away(token) & voc_dict.keys()

def _find_most_common_correct_token_spelling(token):
    candidates = _get_candidates(token)
    if candidates:
        most_common_token = None
        max_count = 0
        for candidate in candidates:
            candidate_count = voc_dict[candidate]
            if candidate_count > max_count:
                most_common_token = candidate
                max_count = candidate_count
        return most_common_token
    else:
        return None

def correct_spelling(tokens):
    res = []
    for i in range(len(tokens.split())):
        token = tokens.split()[i]
        if _is_known(token) and voc_dict[token]>=50:
            res.append(token)
        else:
            correct_token = _find_most_common_correct_token_spelling(token)
            if correct_token is not None:
                res.append(correct_token)
    return ' '.join(res)


'''
    ======================================================
                    query suggestion
    ======================================================
'''

def gen_next(model, tokens):
    # res_list = []
    # res_list.append(tokens)
    tok = tokens.split()[-1]
    # tok_sum = sum(voc_dict.values())
    # num_tok = voc_dict[tok]

    res_dict = {}
    for bigram in model:
        bi_list = bigram.split()
        if tok == bi_list[0]:
            res_dict[bigram] = model[bigram]

    sorted_dict = {k: v for k, v in sorted(res_dict.items(), key=lambda x: x[1], reverse=True)}

    # tokens.join(list(sorted_dict.keys())[0])
    sen = tokens + ' ' + list(sorted_dict.keys())[0].split()[1]



    return sen


def query_suggestion(tokens):
    model = _2gram_model

    res = []
    res.append(tokens)

    sen1 = gen_next(model, tokens)

    sen2 = gen_next(model, sen1)
    res.append(sen1)
    res.append(sen2)

    return res




if __name__ == '__main__':
    # print(correct_spelling("nevar"))
    start = time.time()
    # print(voc_dict['nevar if i cann loove youy and whan i was your loie'])
    print(correct_spelling('nevar if i cann loove youy and whan i was your loie'))
    end = time.time()
    print(end - start)
    print(len(voc_dict))

    '''
    
        query suggestion test
    '''

    # print(gen_next(_2gram_model, 'i love'))
    a = time.time()
    str1 = gen_next(_2gram_model, 'if i know love you my')
    print(str1)


    str2 = gen_next(_2gram_model, str1)
    print(str2)

    str3 = gen_next(_2gram_model, str2)
    print(str3)

    print(time.time() - a)

    b = time.time()

    print(query_suggestion('what'))
    print(time.time() - b)








