# -*- coding: utf-8 -*-
"""
# 1. 启动所有爬虫
# scrapy list
# 每个爬虫执行

## 启动某个爬虫
## 渲染单个页面

每个爬虫生成的 csv 文件名按照 2014-10-01-spider_name.csv

# 2. 生成 index 文件

# 3. 重启 web server

"""

import logging
import logging.handlers
import os
import datetime


CHRYSOLOPHUS_PROJECT_ROOT_DIR = os.environ['CHRYSOLOPHUS_PROJECT_ROOT_DIR']
LOG_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'log')
SRC_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'src')

logging.basicConfig(level=logging.ERROR)
log_name = os.path.join(LOG_FILE_DIR, "run.log")

file_handler = logging.handlers.RotatingFileHandler(log_name,
                                                    maxBytes=104857600,  # 100MB
                                                    backupCount=5)
file_handler.setLevel(level=logging.ERROR)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      datefmt="%d-%m-%Y %H:%M:%S"))

logger = logging.getLogger("run")
logger.addHandler(file_handler)


def _delete_file(file_path):
    rm_cmd = '''rm -rf %s''' % file_path

    try:
        os.system(rm_cmd)
    except:
        logger.error('Deleting old file: %s' % file_path, exc_info=True)
        return False

def mkdir_for_today():
    def _make_multilevel_dir(dir_path):
        mkdir_cmd = '''mkdir -p %s''' % dir_path

        try:
            os.system(mkdir_cmd)
        except:
            logger.error('Building dir structure', exc_info=True)
            return False

        return True

    global CHRYSOLOPHUS_PROJECT_ROOT_DIR

    _STATIC_CSV_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'static/csv')

    csv_dir_path = os.path.join(_STATIC_CSV_DIR,
                                datetime.datetime.now().strftime("%Y/%m/%d"))

    _make_multilevel_dir(csv_dir_path)

    _STATIC_HTML_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'static/html')

    html_dir_path = os.path.join(_STATIC_HTML_DIR,
                                 datetime.datetime.now().strftime("%Y/%m/%d"))

    _make_multilevel_dir(html_dir_path)

    return csv_dir_path, html_dir_path


def crawl(spider_name, output_dir):
    global SRC_FILE_DIR
    crawl_src_dir = os.path.join(SRC_FILE_DIR, 'crawl')
    csv_name = '.'.join([spider_name, 'csv'])
    output_csv = os.path.join(output_dir, csv_name)
    _delete_file(output_csv)

    crawl_cmd = '''cd %s && scrapy crawl %s -t csv -o %s ''' % (crawl_src_dir
                                                                , spider_name
                                                                , output_csv)

    try:
        os.system(crawl_cmd)
    except:
        logger.error('Crawling ...', exc_info=True)

    return output_csv


def get_all_spiders():
    global SRC_FILE_DIR
    crawl_src_dir = os.path.join(SRC_FILE_DIR, 'crawl/crawl')

    list_spider_cmd = '''cd %s && scrapy list ''' % crawl_src_dir
    _raw_output = os.popen(list_spider_cmd).read()
    spider_list = [__str for __str in _raw_output.split('\n') if __str != '']
    return spider_list


def render(spider_name, input_csv, output_dir):
    global SRC_FILE_DIR
    export_src_dir = os.path.join(SRC_FILE_DIR, 'export')
    html_name = '.'.join([spider_name, 'html'])
    output_html = os.path.join(output_dir, html_name)
    _delete_file(output_html)

    export_cmd = '''cd %s && python csv2html.py %s %s''' % (export_src_dir
                                                            , input_csv
                                                            , output_html)

    try:
        os.system(export_cmd)
    except:
        logger.error('Rending ...', exc_info=True)

    return output_html


if __name__ == '__main__':
    today_csv_dir, today_html_dir = mkdir_for_today()

    spiders = get_all_spiders()
    for spider in spiders:
        today_csv_file = crawl(spider, today_csv_dir)
        today_html_file = render(spider, today_csv_file, today_html_dir)
