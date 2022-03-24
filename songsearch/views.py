import time
import numpy as np

from flask import render_template, request, url_for, redirect, flash, escape

from songsearch import app, db
from songsearch.search import parse

@app.route('/', methods=['GET', 'POST'])
def index():
    start_time = time.time()

    if request.method == 'POST':
        content = request.form.get('content')
        if not content or len(content) > 60:
            flash('Invalid search input.')
            return redirect(url_for('index'))
        return redirect(url_for('search', content=escape(content), page=1))

    runtime = round(time.time() - start_time + 0.000005, 5)

    random_pipe = [{ '$sample': { 'size': 10 } }]
    songs = list(db.songs.aggregate(random_pipe))

    return render_template('index.html', songs=songs, runtime=runtime)

@app.route('/search/<content>/<page>', methods=['GET', 'POST'])
def search(content, page):
    page_num = 20
    page_int = [0 + int(page) * page_num, (int(page) + 1) * page_num]
    song_num = 0
    songs = []

    if request.method == 'POST':
        new_content = request.form.get('content')
        if not new_content or len(new_content) > 60:
            flash('Invalid search input.')
            return redirect(url_for('search', content=content), page=page)
        return redirect(url_for('search', content=escape(new_content), page=1))

    songs_cursor, sorted_dict, runtime = parse(content, 'key')

    for song in songs_cursor:
        if song_num == page_int[1]:
            break
        if song_num >= page_int[0]:
            songs.append(song)
        song_num += 1

    # start_time = time.time()

    if len(songs) == 0:

        # runtime = round(time.time() - start_time, 5)

        return render_template('no_results.html', runtime=runtime, keep_input=content)

    # find best and first match lyric
    lyrics = songs[0]['lyrics'].replace("\r", "").split('\n')
    lyrics = np.array([x for x in lyrics if x])
    sort_sen = {k: v for k, v in sorted(sorted_dict[songs[0]['title']].items(), key=lambda x: len(x[1]), reverse=True)}
    pos = int(list(sort_sen.items())[0][0])

    # boundary judgment
    if pos == 0:
        pos = 1
    elif (pos + 2) >= lyrics.shape[0]:
        pos = lyrics.shape[0] - 1
    lyrics_3 = lyrics[pos-1:pos+2]

    # runtime = round(time.time() - start_time, 5)

    if len(songs) == 1:
        return render_template('search.html', lyrics_3=lyrics_3, best=songs[0], songs=[], runtime=runtime, keep_input=content)

    return render_template('search.html', lyrics_3=lyrics_3, best=songs[0], songs=songs[1:], runtime=runtime, keep_input=content)

@app.route('/song/detail/<ObjectId:song_id>')
def detail(song_id):
    song = db.songs.find_one_or_404({"_id": song_id})
    lyrics = song['lyrics'].split('\n')
    return render_template('detail.html', song=song, lyrics=lyrics)

# @app.route('/search/<type>/<content>/<page>', methods=['GET'])
# def search_type(type, content, page):
#     page_num = 20
#     page_int = [0 + int(page) * page_num, (int(page) + 1) * page_num]
#     song_num = 0
#     songs = []

#     songs_cursor, sorted_dict, runtime = parse(content, type)

#     for song in songs_cursor:
#         if song_num == page_int[1]:
#             break
#         if song_num >= page_int[0]:
#             songs.append({'title': song['title'], 'artist':song['artist'], 'lyrics': song['lyrics']})
#         song_num += 1

#     if len(songs) == 0:
#         return {'songs': songs, 'query_time': runtime}

#     for i, song in enumerate(songs):
#         # find best and first match lyric
#         lyrics = song['lyrics'].replace("\r", "").split('\n')
#         lyrics = np.array([x for x in lyrics if x])
#         sort_sen = {k: v for k, v in sorted(sorted_dict[song['title']].items(), key=lambda x: len(x[1]), reverse=True)}
#         pos = int(list(sort_sen.items())[0][0])

#         # boundary judgment
#         songs[i]['sen_pos'] = 1
#         if pos == 0:
#             pos = 1
#             songs[i]['sen_pos'] = 0
#         elif (pos + 2) >= lyrics.shape[0]:
#             pos = lyrics.shape[0] - 1
#             songs[i]['sen_pos'] = 2

#         lyrics_3 = lyrics[pos-1:pos+2]
#         songs[i]['lyrics_3'] = '\n'.join(lyrics_3)


#     return {'songs': songs, 'query_time': runtime}

@app.route('/search/<type>/<content>/<page>', methods=['GET'])
def search_type(type, content, page):

    songs, sorted_dict, runtime = parse(content, type)

    if len(songs) == 0:
        return {'songs': songs, 'query_time': runtime}

    for i, song in enumerate(songs):
        # find best and first match lyric
        lyrics = song['lyrics'].replace("\r", "").split('\n')
        lyrics = np.array([x for x in lyrics if x])
        sort_sen = {k: v for k, v in sorted(sorted_dict[song['title']].items(), key=lambda x: len(x[1]), reverse=True)}
        pos = int(list(sort_sen.items())[0][0])

        # boundary judgment
        songs[i]['sen_pos'] = 1
        if pos == 0:
            pos = 1
            songs[i]['sen_pos'] = 0
        elif (pos + 2) >= lyrics.shape[0]:
            pos = lyrics.shape[0] - 1
            songs[i]['sen_pos'] = 2

        lyrics_3 = lyrics[pos-1:pos+2]
        songs[i]['lyrics_3'] = '\n'.join(lyrics_3)


    return {'songs': songs, 'query_time': runtime}