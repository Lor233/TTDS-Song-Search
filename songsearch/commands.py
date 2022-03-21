import click, json
from tqdm import tqdm

from songsearch import app, db
from songsearch.search import invertedIndex

@app.cli.command()
def clear():
    # Clear the collection
    db.songs.delete_many({})
    db.temp.delete_many({})
    db.words.delete_many({})

    click.echo('Collection cleared.')

@app.cli.command()
def forge():
    # Generate fake data
    # path = './artist-page.json'
    path = './songs_combine.json'
    with open(path, 'r+', encoding='utf-8') as f:
        songs = json.load(f)

    for s in tqdm(songs):
        db.songs.insert_one(s)

    click.echo('Generation done.')

@app.cli.command()
def generateindex():
    invertedIndex()

    click.echo('Inverted Index Generated.')

# @app.cli.command()
# def read():
#     with open('./artist-page.json','r+') as f:
#         songs = json.load(f)

#     click.echo(songs[0])

