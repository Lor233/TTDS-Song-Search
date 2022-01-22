import scrapy


class LyricsSpider(scrapy.Spider):
    name = "artist"
    start_urls = [
        'https://www.lyrics.com/artist/A-5-C-V-Maurice-Avatar/2137939183',
    ]

    def parse(self, response):
        for url in response.xpath('//td/strong/a/@href').getall():
            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback=self.parse_song)

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

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)