import click, json

from songsearch import app, db
# from songsearch.search import invertedIndex

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

    click.echo('Generation done.')

# @app.cli.command()
# def generateindex():
#     invertedIndex()

#     click.echo('Inverted Index Generated.')

@app.cli.command()
def read():
    with open('./artist-page.json','r+') as f:
        songs = json.load(f)

    click.echo(songs[0])

