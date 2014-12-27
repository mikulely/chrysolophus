# -*- coding: utf-8 -*-
# 湖南政府采购网


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
        "您现在的位置：招标（采购）公告",
        "",
        "http://www.ccgp-hunan.gov.cn/more.cfm?sid=100002001&type=&Page=$n",
        5
    ],

    [
        "您现在的位置：中标（成交）公告",
        "",
        "http://www.ccgp-hunan.gov.cn/more.cfm?sid=100002002&type=&Page=$n",
        10
    ],

]

class HuNanTenderSpider(scrapy.Spider):
    name = "hunan"

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
