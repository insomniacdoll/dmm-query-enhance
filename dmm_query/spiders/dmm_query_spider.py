# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from dmm_query.items import DmmQueryItem
from scrapy.http import Request

class DmmQuerySpider(Spider):
  name = "DmmSingleQuery"
  allowed_domains = ["dmm.co.jp"]
  start_url_template = "http://www.dmm.co.jp/search/=/searchstr=%s%%20%s/n1=FgRCTw9VBA4GAVhfWkIHWw__/n2=Aw1fVhQKX1ZRAlhMUlo5QQgBU1lR/"
  start_urls = [
    "http://www.dmm.co.jp/search/=/searchstr=rbd%20550/n1=FgRCTw9VBA4GAVhfWkIHWw__/n2=Aw1fVhQKX1ZRAlhMUlo5QQgBU1lR/"
  ]
  # directory = "/home/pi/dmm_query/dest"
  directory = "/cygdrive/c/Download/zAdult/temp"

  def __init__(self, publisher=None, id=None, *args, **kwargs):
    super(DmmQuerySpider, self).__init__(*args, **kwargs)
    if publisher != None and id != None:
      self.start_urls = [self.start_url_template % (publisher, id)]
      self.publisher = publisher
      self.id = id


  def parse(self, response):
    sel = Selector(response)
    found_list = sel.xpath('//p[@class="tmb"]')
    for found in found_list:
      link_list = found.xpath('a/@href').extract()
      for link in link_list:
        print link
        yield Request(link, cookies={'cklg': 'ja'}, meta={'dont_merge_cookies': True}, callback=self.parseDetail)

  def parseDetail(self, response):
    sel = Selector(response)
    items = []
    item = DmmQueryItem()
    item['publisher'] = self.publisher
    item['id'] = self.id
    item['link'] = response.url
    item['filename'] = "_NonExists"
    item['directory'] = self.directory
    item['cover'] = sel.xpath('//a[@name="package-image"]/@href').extract()[0]
    actress_list = sel.xpath('//span[@id="performer"]/a/text()').extract()
    for actress in actress_list:
      item['actress'] = actress

    item['title'] = sel.xpath('//h1[@id="title"]/text()').extract()[0]
    item['productId'] = sel.xpath(u'//table[@class="mg-b20"]/tr/td[contains(text(),"品番：")]/following-sibling::td/text()').extract()[0]
    thumbnail_list = sel.xpath('//div[@id="sample-image-block"]/a/img/@src').extract()
    thumbnail_large_list = []
    for thumbnail in thumbnail_list:
      thumbnail_large = thumbnail.replace('-', 'jp-')
      thumbnail_large_list.append(thumbnail_large)

    item['thumbnails'] = thumbnail_large_list

    print item['cover']
    print item['actress']
    print item['title']
    print item['productId']
    print item['link']
    print item['thumbnails']
    items.append(item)
    return items

