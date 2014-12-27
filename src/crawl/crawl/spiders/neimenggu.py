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
        "阿拉善政府采购网 首页>>招标公告 ",
        "",
        "http://www.als.gov.cn/zfcg/zhaobiao/index_$n.shtml",
        20
    ],

    [
        "阿拉善政府采购网 首页>>询价采购公示公告 ",
        "",
        "http://www.als.gov.cn/zfcg/xjcg/index_$n.shtml",
        20
    ],

    [
        "阿拉善政府采购网 首页>>中标公告",
        "",
        "http://www.als.gov.cn/zfcg/zbgg/index_$n.shtml" ,
        20
    ],

    [
        "阿拉善政府采购网 首页>>单一来源公示公告 ",
        "",
        "http://www.als.gov.cn/zfcg/dyly/index_$n.shtml",
        20
    ],

    [
        "阿拉善政府采购网 首页>>竞争性谈判公示公告 ",
        "",
        "http://www.als.gov.cn/zfcg/jzxtp/index_$n.shtml",
        10
    ],

]

class NeiMengGuTenderSpider(scrapy.Spider):
    name = "neimenggu"

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
