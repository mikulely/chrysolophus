# -*- coding: utf-8 -*-


import string
import urlparse
import logging
import logging.handlers
import os


CHRYSOLOPHUS_PROJECT_ROOT_DIR = os.environ['CHRYSOLOPHUS_PROJECT_ROOT_DIR']
LOG_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'log')
SRC_FILE_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'src')

logging.basicConfig(level=logging.ERROR)
log_name = os.path.join(LOG_FILE_DIR, "url_helper.log")

file_handler = logging.handlers.RotatingFileHandler(log_name,
                                                    maxBytes=104857600,  # 100MB
                                                    backupCount=5)
file_handler.setLevel(level=logging.ERROR)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      datefmt="%d-%m-%Y %H:%M:%S"))

logger = logging.getLogger("run")
logger.addHandler(file_handler)


def build_abs_url(base_url, relative_url):
    try:
        url_whole = urlparse.urljoin(base_url, relative_url)
    except:
        logger.error(exc_info=True)
    return url_whole


def _build_metadata(url_info):
    assert len(url_info) == 4
    url_description, base_url, next_template, page_count = url_info
    url_metadata_template = {
        "description": unicode(url_description, 'utf8'),
        "index_url": base_url,
        "follow_url_template": string.Template(next_template),
        "pages": page_count,
        }
    return url_metadata_template


def build_url_list(url_metadata):
    url_metadata_list = [_build_metadata(_each_metadata) for _each_metadata in url_metadata]
    final_url_list = []

    if url_metadata_list:
        for metadata in url_metadata_list:
            if metadata['index_url']:
                final_url_list.append(metadata['index_url'])
            if isinstance(metadata['pages'], int):
                start, last = 1, metadata['pages']
            elif isinstance(metadata['pages'], list):
                start, last = metadata['pages']
            if last > 0 and metadata['follow_url_template'] != u'':
                for i in range(start, last + 1):
                    new_url = metadata['follow_url_template'].substitute(n=i)
                    logger.info('New url: %s' % new_url)
                    try:
                        final_url_list.append(new_url)
                    except:
                        logger.error(exc_info=True)

    assert final_url_list is not []
    return final_url_list

