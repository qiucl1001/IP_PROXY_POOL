# encoding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import sys
from ip_pool.db import RedisClient
from ip_pool.crawler import Crawler
from ip_pool.settings import POOL_UPPER_THRESHOLD, CRAWLER_FREE_ENABLED, CRAWLER_MONEY_ENABLED


class Getter(object):
    """
    有了Crawler类之后，在定义一个Getter类，
    用来动态地调用所有以crawl_开头的方法，
    然后获取到的代理，将其加入数据库中保存起来。
    """
    def __init__(self):
        """初始化"""
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断代理池是否溢出
        :return: 返回判断结果
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行...")
        if not self.is_over_threshold():
            if CRAWLER_FREE_ENABLED:
                for callback_label in range(self.crawler.__CrawlFuncCount__):
                    callback = self.crawler.__CrawlFunc__[callback_label]
                    proxies = self.crawler.get_proxies(callback)
                    sys.stdout.flush()
                    for proxy in proxies:
                        self.redis.add(proxy)
            elif CRAWLER_MONEY_ENABLED:
                for callback_label in range(self.crawler.__MoneyFuncCount__):
                    callback = self.crawler.__MoneyFunc__[callback_label]
                    proxies = self.crawler.get_proxies(callback)
                    sys.stdout.flush()
                    for proxy in proxies:
                        self.redis.add(proxy)



