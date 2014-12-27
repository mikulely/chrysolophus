# -*- coding: utf-8 -*-
# 识别标题
#
# Created: 2014-10-15 22:36
# Copyright: (C) 2014 Jiaying Ren  mikulely@gmail.com


import logging
import logging.handlers
import os


#import jieba


import crawl.keywords as keywords


CHRYSOLOPHUS_PROJECT_ROOT_DIR = os.environ['CHRYSOLOPHUS_PROJECT_ROOT_DIR']
LOG_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'log')
SRC_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'src')

logging.basicConfig(level=logging.ERROR)
log_name = os.path.join(LOG_FILE_DIR, "title_helpers.log")

file_handler = logging.handlers.RotatingFileHandler(log_name,
                                                    maxBytes=104857600,  # 100MB
                                                    backupCount=5)
file_handler.setLevel(level=logging.ERROR)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      datefmt="%d-%m-%Y %H:%M:%S"))

logger = logging.getLogger("title_helpers.log")
logger.addHandler(file_handler)


class TitleTypeEnum(object):
    awareded, dropped, required, ignored = range(4)


class ProductTypeEnum(object):
    solar, power, lamp, ignored = range(4)


ProductTypeCN = {
        ProductTypeEnum.solar: unicode('太阳能', 'utf8'),
        ProductTypeEnum.power: unicode('电池', 'utf8'),
        ProductTypeEnum.lamp: unicode('路灯', 'utf8'),
}

#def _tokenize(text):
#    tokens = list(jieba.cut(text, cut_all=False))

def sanitize_title(title):
    """
    1. 先把字串里的标点符号处理点，分句子
    2. 在放入 jieba 分词
    """

def get_product_type(title):
    """
    判断标题的类型
    """
    if any(title.find(each_type) > 0 for each_type in keywords.ignored_solar_type):
        return ProductTypeEnum.ignored
    if any(title.find(each_type) > 0 for each_type in keywords.ignored_power_type):
        return ProductTypeEnum.ignored
    # FIXME 引入分词之后，把招标信息类型的判断 get_title_type
    if any(title.find(each_type) > 0 for each_type in keywords.dropped):
        return ProductTypeEnum.ignored
    if any(title.find(each_type) > 0 for each_type in keywords.solar):
        return ProductTypeEnum.solar
    if any(title.find(each_type) > 0 for each_type in keywords.power):
        return ProductTypeEnum.power
    if any(title.lower().find(each_type) > 0 for each_type in keywords.lamp):
        #        ^^^^^^ 注意因为路灯里的关键字 LED 为英文，注意大小写
        return ProductTypeEnum.lamp

    logger.critical('Unmatched title: %s' % title)
    return ProductTypeEnum.ignored


def get_title_type(title):
    if any(title.find(each_type) > 0 for each_type in keywords.awarded):
        return TitleTypeEnum.awareded
    if any(title.find(each_type) > 0 for each_type in keywords.required):
        return TitleTypeEnum.required
    return TitleTypeEnum.ignored

def extract_link_title(link):
    result, title = False, unicode('', 'utf8')

    has_extract_from_title_attr = link.xpath('@title').extract()
    if has_extract_from_title_attr:
        result, title = True, has_extract_from_title_attr[0].strip()
        # 真的要做 NPL 的时候需要考虑，title 里可能有标点
    else:
        has_extract_from_text = link.xpath('text()').extract()
        if has_extract_from_text:
            result, title = True, has_extract_from_text[0].strip()

    return result, title
