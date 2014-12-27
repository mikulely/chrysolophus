# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from crawl.title_helpers import ProductTypeCN

class TenderPipeline(object):

    def __init__(self):
        self.tender_seen = set()

    def process_item(self, item, spider):
        if item['title'] in self.tender_seen:
            pass
        else:
            self.tender_seen.add(item['title'])
            item['product_type'] = ProductTypeCN[item['product_type']]
            return item
