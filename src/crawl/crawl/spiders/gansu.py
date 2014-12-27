# -*- coding: utf-8 -*-
# 甘肃政府采购网 http://www.ccgp-gansu.gov.cn/templet/default/index.html


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
        "首页 >> 采购公告 >> 招标采购公告 >> 公开招标",
        "",
        "http://www.ccgp-gansu.gov.cn/votoonadmin/article/classlist.jsp?pn=$n&class_id=138",
        20
    ],

    [
        "首页 >> 采购公告 >> 招标采购公告 >> 邀请公告",
        "",
        "http://www.ccgp-gansu.gov.cn/votoonadmin/article/classlist.jsp?pn=$n&class_id=214",
        5
    ],

    [
        "首页 >> 采购公告 >> 中标公告",
        "",
        "http://www.ccgp-gansu.gov.cn/votoonadmin/article/classlist.jsp?pn=$n&class_id=140",
        25
    ],

    [
        "首页 >> 采购公告 >> 成交公告",
        "",
        "http://www.ccgp-gansu.gov.cn/votoonadmin/article/classlist.jsp?pn=$n&class_id=220",
        10
    ],

]

class GanSuTenderSpider(scrapy.Spider):
    name = "gansu"

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
