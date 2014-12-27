# -*- coding: utf-8 -*-
# 福建政府采购网 http://www.ccgp-jiangsu.gov.cn/pub/jszfcg/


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
        "县级公告",
        "",
        "http://www.ccgp-fujian.gov.cn/secpag.cfm?PageNum=$n&&caidan=%B2%C9%B9%BA%B9%AB%B8%E6&level=county",
        20
    ],

    [
        "分散采购公告",
        "",
        "http://www.ccgp-fujian.gov.cn/secpag.cfm?PageNum=$n&&caidan=%B7%D6%C9%A2%B2%C9%B9%BA%B9%AB%B8%E6&level=province&yqgg=0",
        20
    ],


    [
        "省级公告",
        "",
        "http://www.ccgp-fujian.gov.cn/secpag.cfm?PageNum=$n&&caidan=%B2%C9%B9%BA%B9%AB%B8%E6&level=province",
        40
    ],

    [
        "市级公告",
        "",
        "http://www.ccgp-fujian.gov.cn/secpag.cfm?PageNum=$n&&caidan=%B2%C9%B9%BA%B9%AB%B8%E6&level=city",
        20
    ],
]


class FuJianTenderSpider(scrapy.Spider):
    name = "fujian"

    start_urls = build_url_list(_url_metadata)

    tender_link_xpath_pattern = '//td/a'

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
