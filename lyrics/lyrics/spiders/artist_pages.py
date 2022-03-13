import scrapy

class LyricsSpider(scrapy.Spider):
    song_N = 0
    name = "artist-pages"
    start_urls = [
        # 'https://www.lyrics.com/artists/A/99999',
        # 'https://www.lyrics.com/artists/B/99999',
        # 'https://www.lyrics.com/artists/C/99999',
        # 'https://www.lyrics.com/artists/D/99999',
        'https://www.lyrics.com/artists/E/99999',
        # 'https://www.lyrics.com/artists/F/99999',
    ]

    def parse(self, response):
        urls = response.xpath('//td[@class="tal qx"]/a/@href').getall() + response.xpath('//td[@class="tal qx"]/strong/a/@href').getall()
        for url in urls:
            if 'artist-fans' not in url:
                artist_page = response.urljoin(url)
                yield scrapy.Request(artist_page, callback=self.parse_artist)

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_artist(self, response):
        for url in response.xpath('//td/strong/a/@href').getall():
            song_page = response.urljoin(url)
            yield scrapy.Request(song_page, callback=self.parse_song)

    def parse_song(self, response):
        self.song_N += 1
        lyrics = ''
        words = response.xpath('//pre/text()').getall()
        linkwords = response.xpath('//pre/a/text()').getall()
        linkwords.append('')
        for word, linkword in zip(words, linkwords):
            lyrics += word + linkword
        yield {
            'N': self.song_N,
            'title': response.xpath('//hgroup/h1/text()').get(),
            'artist': response.xpath('//h3[@class="lyric-artist"]/a/text()').get(),
            'duration': response.xpath('//div[@class="lyric-details"]/dl/dd[1]/text()').get(),
            'lyrics': lyrics,
        }
