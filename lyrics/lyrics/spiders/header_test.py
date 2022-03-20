import scrapy


class ScrapySpider(scrapy.Spider):
    name = "scrapy_spider"
    allowed_domains = ["httpbin.org"]
    start_urls = (
        # 请求的链接
        "https://httpbin.org/get?show_env=1",
    )

    def parse(self, response):
        # 打印出相应结果 
        print(response.text)


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl scrapy_spider".split())
