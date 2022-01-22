# TTDS Song Search

Lyrics search engine demo project.

## Install Requirements

Before installing packages, it is recommended to configure a virtual environment using [Conda](https://docs.conda.io/en/latest/miniconda.html)

### Install Conda

Here windows conda used.

### Install Scrapy

[Scrapy](https://github.com/scrapy/scrapy) is used to create lyrics spiders.

```
conda install scrapy
conda install protego
```

## Run Spiders Examples

Enter the example project.

```
cd lyrics
```

### Crawl one song

Example song: [Love Is Perverse](https://www.lyrics.com/sublyric/122508/The+Immaculate+Crows/Love+Is+Perverse)

```
scrapy crawl lyrics -O lyrics.json
```

### Crawl songs of one artist

Example artist: [A 5 C V Maurice Avatar](https://www.lyrics.com/artist/A-5-C-V-Maurice-Avatar/2137939183)

```
scrapy crawl artist -O artist.json
```

## Useful Docs

[Scrapy 2.5 documentation¶](https://docs.scrapy.org/en/latest/)