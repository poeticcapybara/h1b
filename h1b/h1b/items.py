# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class H1BItem(scrapy.Item):
    # define the fields for your item here like:
    employer = scrapy.Field()
    jobtitle = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    status = scrapy.Field()
    startdate = scrapy.Field()
    submitdate = scrapy.Field()
