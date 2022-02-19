import time
import numpy as np

from flask import render_template, request, url_for, redirect, flash, escape
from sqlalchemy.sql.expression import func

from songsearch import app, db
from songsearch.models import Song

@app.route('/', methods=['GET', 'POST'])
def index():
    start_time = time.time()
    if request.method == 'POST':
        content = request.form.get('content')
        if not content or len(content) > 60:
            flash('Invalid search input.')
            return redirect(url_for('index'))
        return redirect(url_for('search', content=escape(content)))
    songs = Song.query.order_by(func.random()).limit(13).all()
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
    songs = Song.query.filter(Song.lyrics.like('%%{content}%'.format(content=content))).limit(9).all()

    if len(songs) == 0:
        runtime = round(time.time() - start_time + 0.005, 2)
        return render_template('no_results.html', runtime=runtime)

    # find best and first match lyric
    lyrics = songs[0].lyrics.replace("\r", "").split('\n')
    lyrics = np.array([x for x in lyrics if x])
    pos = [i for i,item in enumerate(lyrics) if content in item][0]
    # boundary judgment
    if pos == 0:
        pos = 1
    elif pos + 2 >= lyrics.shape[0]:
        pos = lyrics.shape[0] - 1
    lyrics_3 = lyrics[pos-1:pos+2]
    runtime = round(time.time() - start_time + 0.005, 2)

    if len(songs) == 1:
        return render_template('search.html', lyrics_3=lyrics_3, best=songs[0], songs=[], runtime=runtime)

    return render_template('search.html', lyrics_3=lyrics_3, best=songs[0], songs=songs[1:], runtime=runtime)

@app.route('/song/detail/<int:song_id>')
def detail(song_id):
    song = Song.query.get_or_404(song_id)
    lyrics = song.lyrics.split('\n')
    return render_template('detail.html', song=song, lyrics=lyrics)

# @app.route('/user/<name>')
# def user_page(name):
#     return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    print(url_for('index'))  # /
    print(url_for('user_page', name='greyli'))  # /user/greyli
    print(url_for('user_page', name='peter'))  # /user/peter
    print(url_for('test_url_for'))  # /test
    print(url_for('test_url_for', num=2))  # /test?num=2
    return 'Test page'