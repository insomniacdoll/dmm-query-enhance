#!/usr/bin/env python
import sys

from twisted.internet import threads, reactor, defer
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher

from dmm_query.spiders.dmm_query_spider import DmmQuerySpider
from dmm_query.spiders.dmm_batch_query_spider import DmmBatchQuerySpider


def setup_crawler(id="550", publisher="rbd"):
    spider = DmmQuerySpider(id, publisher)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

def stop_reactor():
    reactor.stop()

if __name__ == '__main__':

    # pass the args
    id = sys.argv[2]
    publisher = sys.argv[1]

    # regist the stop func
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    
    # start up the spider
    setup_crawler(id, publisher)
    log.start()
    reactor.run()

