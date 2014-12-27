# -*- coding: utf-8 -*-
# 新疆政府采购网 http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/


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
        "新疆维吾尔自治区政府采购网",
        "http://www.xjzfcg.gov.cn/mos/cms/html/1/index.html",
        "",
        0
    ],

    [
        "地州政府采购网",
        "",
        "http://www.xjzfcg.gov.cn/mos/cms/html/$n/index.html",
        [100, 150],
    ],

]

class XinjiangTenderSpider(scrapy.Spider):
    name = "xinjiang"

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
