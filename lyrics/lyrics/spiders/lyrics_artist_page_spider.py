import scrapy


class LyricsSpider(scrapy.Spider):
    name = "artist-page"
    start_urls = [
        'https://www.lyrics.com/artists/A',
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
        lyrics = ''
        words = response.xpath('//pre/text()').getall()
        linkwords = response.xpath('//pre/a/text()').getall()
        linkwords.append('')
        for word, linkword in zip(words, linkwords):
            lyrics += word + linkword
        yield {
            'title': response.xpath('//hgroup/h1/text()').get(),
            'artist': response.xpath('//h3[@class="lyric-artist"]/a/text()').get(),
            'lyrics': lyrics,
        }
