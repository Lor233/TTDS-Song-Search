# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from fake_useragent import UserAgent

import random, time


class LyricsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LyricsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, user_agent='chrome'):
        # self.user_agent = user_agent
        self.user_agent = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        # s = cls(user_agent=crawler.settings.get('MY_USER_AGENT'))
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # agent = random.choice(self.user_agent)
        agent = self.user_agent.random
        request.headers['User-Agent'] = agent

        ref = 'https://www.lyrics.com/artists/' + f'{random.randint(1,1500)}'
        # ref = 'https://www.google.com/' + f'{random.randint(-1500,1)}'
        request.headers['Referer'] = ref

        # proxy = "http://4fe57a46cc4f469c8c40d619908bb954:@proxy.crawlera.com:8011/"
        # request.meta["proxy"] = proxy

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        # if response.status == 403:
        #     print("403 wait 5min:" + proxy)
        #     spider.crawler.engine.pause()
        #     await async_sleep(delay)
        #     spider.crawler.engine.unpause()
        #     return request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TooManyRequestsRetryMiddleware(RetryMiddleware):

    def __init__(self, crawler):
        super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler
        self.user_agent = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        elif response.status == 403:
            self.crawler.engine.pause()
            print(f'{time.asctime( time.localtime(time.time()) )}: 403 wait Start')
            time.sleep(300) # If the rate limit is renewed in a minute, put 60 seconds, and so on.
            print(f'{time.asctime( time.localtime(time.time()) )}: 403 wait End')
            self.crawler.engine.unpause()

            agent = self.user_agent.random
            request.headers['User-Agent'] = agent

            # ref = 'https://www.lyrics.com/' + f'{random.randint(1,1500)}'
            ref = 'https://www.lyrics.com/artists/' + f'{random.randint(1,1500)}'
            # ref = 'https://www.google.com/' + f'{random.randint(-1500,1)}'
            request.headers['Referer'] = ref

            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        elif response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response 
