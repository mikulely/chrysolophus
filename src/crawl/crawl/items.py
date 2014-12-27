# -*- coding: utf-8 -*-


import scrapy


class TenderItem(scrapy.Item):
    """" 招标信息定义 """
    #: 标书 URL
    url = scrapy.Field()
    #: 招标产品的类型
    product_type = scrapy.Field()
    #: 标书标题
    title = scrapy.Field()
