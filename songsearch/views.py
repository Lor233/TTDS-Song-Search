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
        return redirect(url_for('search', content=escape(content)))

    random_pipe = [{ '$sample': { 'size': 13 } }]
    songs = list(db.songs.aggregate(random_pipe))
    runtime = round(time.time() - start_time + 0.005, 2)

    return render_template('index.html', songs=songs, runtime=runtime)

@app.route('/search/<content>', methods=['GET', 'POST'])
def search(content):
    start_time = time.time()

    if request.method == 'POST':
        new_content = request.form.get('content')
        if not new_content or len(new_content) > 60:
            flash('Invalid search input.')
            return redirect(url_for('search', content=content))
        return redirect(url_for('search', content=escape(new_content)))

    songs = list(parse(content))

    if len(songs) == 0:
        runtime = round(time.time() - start_time + 0.005, 2)
        return render_template('no_results.html', runtime=runtime, keep_input=content)

    # find best and first match lyric
    lyrics = songs[0]['lyrics'].replace("\r", "").split('\n')
    lyrics = np.array([x for x in lyrics if x])
    print(len(songs))
    print(songs[0]['match_titles'])
    pos = songs[0]['match_titles'][0]['sen_pos'] if len(songs[0]['match_titles'])!=0 else 0

    # boundary judgment
    if pos == 0:
        pos = 1
    elif pos + 2 >= lyrics.shape[0]:
        pos = lyrics.shape[0] - 1
    lyrics_3 = lyrics[pos-1:pos+2]
    runtime = round(time.time() - start_time + 0.005, 2)

    if len(songs) == 1:
        return render_template('search.html', lyrics_3=lyrics_3, best=songs[0], songs=[], runtime=runtime, keep_input=content)

    return render_template('search.html', lyrics_3=lyrics_3, best=songs[0], songs=songs[1:], runtime=runtime, keep_input=content)

@app.route('/song/detail/<ObjectId:song_id>')
def detail(song_id):
    song = db.songs.find_one_or_404({"_id": song_id})
    lyrics = song['lyrics'].split('\n')
    return render_template('detail.html', song=song, lyrics=lyrics)