# Lyrics spider
Lyrics spider runing.

## Install Requirements
Before installing packages, it is recommended to configure a virtual environment using [Conda](https://docs.conda.io/en/latest/miniconda.html)

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

### Crawl songs of one page 'A' artists
Example page: [artists start with 'a' (1st page)](https://www.lyrics.com/artists/A)
```
scrapy crawl artist-page -O artist-page.json -s LOG_FILE=scrapy.log 
```

### Crawl songs of all pages 'A' artists
```
scrapy crawl artist-pages -O artist-pages.json -s LOG_FILE=scrapy_s.log
```

## Useful Docs

[Scrapy 2.5 documentation¶](https://docs.scrapy.org/en/latest/)