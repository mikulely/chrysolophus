#!/bin/python
# -*- coding: utf-8 -*-
# 将 csv 导出成 html

import csv
import datetime
import logging
import logging.handlers
import os
import sys


import jinja2


reload(sys)
sys.setdefaultencoding('utf-8')


CHRYSOLOPHUS_PROJECT_ROOT_DIR = os.environ['CHRYSOLOPHUS_PROJECT_ROOT_DIR']
LOG_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'log')


logging.basicConfig(level=logging.ERROR)
log_name = os.path.join(LOG_FILE_DIR, "csv2html.log")

file_handler = logging.handlers.RotatingFileHandler(log_name,
                                                    maxBytes=104857600,  # 100MB
                                                    backupCount=5)
file_handler.setLevel(level=logging.ERROR)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      datefmt="%d-%m-%Y %H:%M:%S"))

logger = logging.getLogger("csv2html")
logger.addHandler(file_handler)


def is_invalid_path(path):
    try:
        os.path.isabs(path)
    except:
        logger.error(exc_info=True)
        return True

    return False


def sanitize_csv(csv_file):
    sanitized_list = []
    for line in csv_file:
        if line == ['url', 'product_type', 'title']:
            pass
        else:
            sanitized_list.append(line)
    return sanitized_list


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if any(is_invalid_path(_each) for _each in [input_file, output_file]):
        logger.error('Args invalid')

    today_ts = str(datetime.datetime.utcnow().date())

    with open(input_file, 'rb') as csv_file:
        tender_in_csv = csv.reader(csv_file)
        sanitized_csv = sanitize_csv(tender_in_csv)
        if sanitized_csv:

            template_loader = jinja2.FileSystemLoader("templates")
            template_env = jinja2.Environment(loader=template_loader)
            _TENDER_TEMPLATE_FILE = "tender.html"
            template = template_env.get_template(_TENDER_TEMPLATE_FILE)
            template_vars = {"tender_in_csv": sanitized_csv,
                             "title": today_ts,
                             "today": today_ts}

            with open(output_file, 'w') as out:
                outputText = template.render(template_vars)
                out.write(outputText)
        else:
            logger.info('Skipping empty csv: %s' % input_file)
