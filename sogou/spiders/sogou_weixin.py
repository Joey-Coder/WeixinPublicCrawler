# -*- coding: utf-8 -*-
import scrapy
import logging
from sogou.items import ArticleItem, AccountItem
import datetime
import json
from selenium import webdriver
import time
from sogou.settings import MAX_PAGE


class SogouWeixinSpider(scrapy.Spider):
    name = 'sogou_weixin'
    # allowed_domains = ['http://weixin.sogou.com']
    # start_urls = ['http://http://weixin.sogou.com/']
    logger = logging.getLogger(__name__)
    page_article_url = 'https://weixin.sogou.com/weixin?query={word}&_sug_type_=&s_from=input&_sug_=n&type=2&page={page}&ie=utf8'
    page_account_url = 'https://weixin.sogou.com/weixin?query={word}&_sug_type_=&s_from=input&_sug_=n&type=1&page={page}&ie=utf8'
    test_url = 'https://weixin.sogou.com/weixin?query=%E5%90%89%E4%BB%96&_sug_type_=&sut=3885&lkt=5%2C1542871482953%2C1542871486820&s_from=input&_sug_=n&type=2&sst0=1542871486923&page=20&ie=utf8&w=01019900&dr=1'

    # with open('/Users')

    def start_requests(self):
        # 输入想爬取的信息
        word = input('please input the word for search:')
        # 文章类抓取链接
        yield scrapy.Request(url=self.page_article_url.format(word=word,page=1),callback=self.article_parse,meta={'page':1,'word':word,'retry_times':True},dont_filter=True)
        # 公众号账号抓取链接
        # yield scrapy.Request(url=self.page_account_url.format(word=word, page=1), callback=self.account_parse,
        #                      meta={'page': 1, 'word': word, 'retry_times': True}, dont_filter=True)

    '''
        文章抓取parse
    '''

    def article_parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        cookies = response.request.cookies
        word = response.meta.get('word')
        page = response.meta.get('page')
        # handle_httpstatus_list = [302]
        self.logger.debug('[+] status_code : %s' % response.status)
        infos = response.xpath('//ul[@class="news-list"]//li//div[@class="txt-box"]')
        for info in infos:
            item = ArticleItem()
            item['title'] = ''.join(info.xpath('./h3/a/text()').extract())
            item['weixin_name'] = info.xpath('.//a[@class="account"]/text()').extract_first()
            time = info.xpath('.//span[@class="s2"]//text()').re_first('document.write\(timeConvert\(\'(.*?)\'\)\)')
            if time:
                d_time = datetime.datetime.fromtimestamp(int(time))
                s_time = d_time.strftime("%Y-%m-%d %H:%M:%S")
            item['time'] = s_time if time else None
            item['content'] = ''.join(info.xpath('.//p[@class="txt-info"]//text()').extract())
            item['url'] = info.xpath('./h3/a/@href').extract_first()
            yield item
            # self.logger.debug(item)

        if page < MAX_PAGE:
            page += 1
            proxy = response.meta.get('proxy')
            yield scrapy.Request(url=self.page_article_url.format(word=word, page=page), callback=self.article_parse,
                                 cookies=cookies, meta={'page': page, 'word': word, 'proxy': proxy}, dont_filter=True)

    '''
        账号抓取parse
    '''

    def account_parse(self, response):
        cookies = response.request.cookies
        word = response.meta.get('word')
        page = response.meta.get('page')
        self.logger.debug('[+] status_code : %s' % response.status)
        infos = response.xpath('//div[@class="news-box"]/ul[@class="news-list2"]//li')
        for info in infos:
            item = AccountItem()
            item['name'] = ''.join(info.xpath('./div//a//text()').extract())
            item['account'] = info.xpath('./div//label[@name="em_weixinhao"]/text()').extract_first()
            item['recommend'] = ''.join(info.xpath('./dl[1]/dd//text()').extract())
            item['Authentication'] = ''.join(info.xpath('./dl[2]/dd//text()').extract())
            item['article_lately'] = ''.join(info.xpath('./dl[3]/dd/a//text()').extract())
            time = info.xpath('./dl[3]/dd/span//text()').re_first('document.write\(timeConvert\(\'(.*?)\'\)\)')
            if time:
                d_time = datetime.datetime.fromtimestamp(int(time))
                s_time = d_time.strftime("%Y-%m-%d %H:%M:%S")
            item['time'] = s_time if time else None

            yield item

        if page < MAX_PAGE:
            page += 1
            proxy = response.meta.get('proxy')
            yield scrapy.Request(url=self.page_account_url.format(word=word, page=page), callback=self.account_parse,
                                 cookies=cookies, meta={'page': page, 'word': word, 'proxy': proxy}, dont_filter=True)
