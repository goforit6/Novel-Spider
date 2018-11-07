# -*- coding: utf-8 -*-
import scrapy
from Quanshu.items import QuanshuItem
import os


class QuanshuSpider(scrapy.Spider):
    name = 'quanshu'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://quanshuwang.com/']

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26'
        }

    def start_requests(self):
        url = 'http://www.quanshuwang.com/'
        yield scrapy.Request(url, callback=self.parse_kindof, headers=self.headers)

    def parse_kindof(self, response):
        """解析所有小说的类目及对应链接"""
        kind_links = response.xpath("//ul[@class='channel-nav-list']//li/a/@href").extract()
        # kind_names = response.xpath("//ul[@class='channel-nav-list']//li/a/text()").extract()
        for link in kind_links:
            yield scrapy.Request(link, callback=self.parse_novel_pages, headers=self.headers)

    def parse_novel_pages(self, response):
        """解析当前类目下的小说页数"""
        # 此类目下的小说一共有多少页
        novel_pages = response.xpath("//div[@id='pagelink']/a[@class='last']/text()").extract_first()
        for novel_page in range(1, int(novel_pages) + 1):
            curent_url = response.url.split('_')[0] + '_' + str(novel_page) + '.html'
            yield scrapy.Request(curent_url, callback=self.parse_novel, headers=self.headers)

    def parse_novel(self, response):
        """解析当前类目下每页所有小说的链接，每个li就是一部小说"""
        novels = response.xpath("//ul[contains(@class, 'seeWell ')]//li")
        for novel in novels:
            # novel_title = novel.xpath("./span/a[1]/text()").extract_first()
            # novel_author = novel.xpath("./span/a[2]/text()").extract_first()
            novel_link = novel.xpath("./span/a[1]/@href").extract_first()
            yield scrapy.Request(novel_link, callback=self.click_begin_read, headers=self.headers)

    def click_begin_read(self, response):
        """访问 “开始阅读” 进入小说详情页的所有章节列表"""
        novel_url = response.xpath("//div[@class='b-oper']/a[1]/@href").extract_first()
        yield scrapy.Request(novel_url, callback=self.parse_chapter, headers=self.headers)

    def parse_chapter(self, response):
        """解析每个章节的url"""
        chapter_links = response.xpath("//div[@class='chapterNum']//li/a/@href").extract()
        chapter_names = response.xpath("//div[@class='chapterNum']//li/a/text()").extract()
        authors = response.xpath("//span[@class='r']/text()").extract()
        novel_title = response.xpath("//strong/text()").extract()
        novel_type = response.xpath("//div[@class='main-index']/a[2]/text()").extract()
        ts = zip(novel_type, novel_title, authors, chapter_names, chapter_links)
        for t in ts:
            request = scrapy.Request(t[-1], callback=self.parse_content, headers=self.headers)
            request.meta['item'] = t[:-1]  # 传递参数过去
            yield request
        # for chapter_link in chapter_links:
        #     yield scrapy.Request(chapter_link, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        """解析当前章节的正文内容"""
        contents = response.xpath("//div[@id='content']/text()").extract()
        content = ''.join(contents)

        # 1. 写入本地文件
        # novel_type, novel_title, author, chapter_name = response.meta['item']  # 接收传递过来的参数
        # filepath = 'test/' + novel_type + '/' + novel_title
        # if not os.path.exists(filepath):
        #     os.makedirs(filepath)
        # filename = filepath + '/' + chapter_name + '.txt'
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(content)

        # 2. 准备存入MongoDB数据库
        item = QuanshuItem()
        item['chapter_content'] = content
        item['typeof'], item['novel_title'], item['author'], item['chapter_name'] = response.meta['item']
        yield item










