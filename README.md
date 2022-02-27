# TTDS Song Search
Lyrics search engine demo project.

## Install Requirements
Before installing packages, it is recommended to configure a virtual environment using [Conda](https://docs.conda.io/en/latest/miniconda.html)
```
pip install -r requirements.txt
```
[Flask](https://github.com/pallets/flask) is used to construct search engine framework.
[Flask-Pymongo](https://github.com/dcrosta/flask-pymongo) is used to connect Flask and MongoDB.

## Run Song Search Engine
Enter the example project.
```
cd songsearch
```
Run the website with Flask.
```
flask run
```

## Useful Docs
[Construct a Watchlist based on Flask¶](https://read.helloflask.com/c0-preface)

[How to Set Up Flask with MongoDB¶](https://www.mongodb.com/compatibility/setting-up-flask-with-mongodb)

[Flask-PyMongo¶](https://flask-pymongo.readthedocs.io/en/latest/)

[PyMongo 4.0.1 Documentation¶](https://pymongo.readthedocs.io/en/stable/)