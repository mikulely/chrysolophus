# -*- coding: utf-8 -*-
# 中国政府集采网 http://www.ccgp.gov.cn


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
        "中国政府采购网 > 采购公告 > 地方标讯 > 公开招标公告",
        "http://www.ccgp.gov.cn/cggg/dfbx/gkzb/default.shtml",
        "http://www.ccgp.gov.cn/cggg/dfbx/gkzb/default_$n.shtml",
        30
    ],

    [
        "中国政府采购网 > 采购公告 > 地方标讯",
        "http://www.ccgp.gov.cn/cggg/dfbx/index.shtml",
        "http://www.ccgp.gov.cn/cggg/dfbx/index_$n.shtml",
        24
    ],

    [
        "中国政府采购网 > 采购公告",
        "http://www.ccgp.gov.cn/cggg/index.shtml",
        "http://www.ccgp.gov.cn/cggg/index_$n.shtml",
        19
    ],

    [
        "中国政府采购网 > 采购公告",
        "http://www.ccgp.gov.cn/cggg/index.shtml",
        "http://www.ccgp.gov.cn/cggg/index_$n.shtml",
        19
    ],

    [
        "中国政府采购网 > 采购公告 > 地方标讯 > 中标公告",
        "http://www.ccgp.gov.cn/cggg/dfbx/zbgg/default.shtml",
        "http://www.ccgp.gov.cn/cggg/dfbx/zbgg/default_$n.shtml",
        25
    ],

    [
        "中共中央直属机关采购中心 > 招标公告",
        "http://zzcg.ccgp.gov.cn/zzcg/cgxx/cggg/H600401index_1.htm",
        "",
        0
    ],

    [
        "中共中央直属机关采购中心 > 中标公告",
        "http://zzcg.ccgp.gov.cn/zzcg/cgxx/jggg/H600402index_1.htm",
        "",
        0
    ],
]


class CCGPTenderSpider(scrapy.Spider):
    name = "ccgp"
    start_urls = build_url_list(_url_metadata)

    tender_link_xpath_pattern = '//ul/li/a'

    def parse(self, response):
        base_url = get_base_url(response)
        # links = response.xpath('//ul[contains(@class, "ulst")]/li/a[contains(@href, "html")]')
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
