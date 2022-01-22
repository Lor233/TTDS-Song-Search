import scrapy


class LyricsSpider(scrapy.Spider):
    name = "html"
    start_urls = [
        'https://www.lyrics.com/sublyric/122508/The+Immaculate+Crows/Love+Is+Perverse',
    ]

    def parse(self, response):
        song = response.url.split("/")[-1]
        filename = f'lyrics-{song}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')