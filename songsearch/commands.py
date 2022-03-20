import click, json
from tqdm import tqdm
import numpy as np

from songsearch import app, db
from songsearch.search import new_data

@app.cli.command()
def clear():
    # Clear the collection
    db.temp.delete_many({})
    db.words.delete_many({})

    click.echo('Collection cleared.')

@app.cli.command()
def forge():
    # Generate fake data
    with open('./artist-page.json','r+') as f:
        songs = json.load(f)

    for s in songs:
        db.songs.insert_one(s)

    click.echo('Fake Data Generation done.')

@app.cli.command()
def index():
    # Generate fake data
    _, inv = new_data('./songs_combine.json')

    # np.save('inv', inv)

    np.save('./lyrics/data/inv', inv)

    click.echo('Index Generation done.')

@app.cli.command()
def combine():
    dict = {}
    num = 0

    for x in tqdm(list(map(chr, range(97, 123)))):
        with open(f'./lyrics/results/{x}.json', 'r+', encoding='utf-8') as f:
            songs = json.load(f)

        for s in songs:
            if not s['title']:
                s['title'] = 'None'
            if not s['artist']:
                s['artist'] = 'None'
            if dict.get(s['title'] + s['artist'], 0) == 0:
                dict[s['title'] + s['artist']] = 1
                db.songs_combine.insert_one({'title':s['title'], 'artist':s['artist'], 'duration':s['duration'], 'lyrics':s['lyrics']})
            else:
                num += 1

    click.echo('Combine done.')
    click.echo(f'Import {len(dict.keys())} songs.')
    click.echo(f'Filter {num} repeat songs.')

# @app.cli.command()
# def generateindex():
#     invertedIndex()

#     click.echo('Inverted Index Generated.')

@app.cli.command()
def read():
    with open('./artist-page.json','r+') as f:
        songs = json.load(f)

    click.echo(songs[0])

