# -*- coding: utf-8 -*-


import scrapy


from crawl.items import TenderItem
from scrapy.utils.response import get_base_url
from crawl.url_helpers import build_abs_url
from crawl.url_helpers import build_url_list
from crawl.title_helpers import get_product_type
from crawl.title_helpers import ProductTypeEnum
from crawl.title_helpers import extract_link_title


_url_metadata = [
    [
        "首页 > 采购公告 > 公开招标 ",
        "http://www.gxgp.gov.cn/cggkzb/index.htm",
        "http://www.gxgp.gov.cn/cggkzb/index_$n.htm",
        10
    ],

    [
        "首页 > 采购公告 > 竞争性谈判",
        "",
        "http://www.gxgp.gov.cn/cgjz/index_$n.htm",
        5
    ],

    [
       "首页 > 采购公告 > 询价采购 ",
       "http://www.gxgp.gov.cn/cgxjcg/index.htm",
       "http://www.gxgp.gov.cn/cgxjcg/index_$n.htm",
       5

    ],

    [
        "首页 > 采购公告 > 单一来源采购",
        "http://www.gxgp.gov.cn/cgdyly/index.htm",
        "http://www.gxgp.gov.cn/cgdyly/index_$n.htm",
        10
    ],
 ]

class GuangXiTenderSpider(scrapy.Spider):
    name = "guangxi"

    start_urls = build_url_list(_url_metadata)

    tender_link_xpath_pattern = '//a'

    def parse(self, response):
        base_url = get_base_url(response)
        links = response.xpath(self.tender_link_xpath_pattern)
        if links:
            for link in links:
                ok, title = extract_link_title(link)
                if ok:
                    product_type = get_product_type(title)
                    if product_type != ProductTypeEnum.ignored:
                        relative_url = link.xpath('@href').extract()[0]
                        url_whole = build_abs_url(base_url, relative_url)
                        tender = TenderItem()
                        tender['title'] = title
                        tender['url'] = url_whole
                        tender['product_type'] = product_type
                        yield tender
