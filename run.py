#!/usr/bin/env python
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from dmm_query.spiders.dmm_query_spider import DmmQuerySpider
from dmm_query.spiders.dmm_batch_query_spider import DmmBatchQuerySpider 
from scrapy.utils.project import get_project_settings
import sys

def setup_crawler(id="550", publisher="rbd"):
    spider = DmmQuerySpider(id, publisher)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

if __name__ == "__main__":
    id = sys.argv[2]
    publisher = sys.argv[1]
    setup_crawler(id, publisher)
    log.start()
    reactor.run()

