import scrapy


class LyricsSpider(scrapy.Spider):
    name = "lyrics"
    start_urls = [
        'https://www.lyrics.com/sublyric/122508/The+Immaculate+Crows/Love+Is+Perverse',
    ]

    def parse(self, response):
        lyrics = ''
        words = response.xpath('//pre/text()').getall()
        linkwords = response.xpath('//pre/a/text()').getall()
        linkwords.append('')
        for word, linkword in zip(words, linkwords):
            lyrics += word + linkword
        yield {
            'lyrics': lyrics,
        }

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)