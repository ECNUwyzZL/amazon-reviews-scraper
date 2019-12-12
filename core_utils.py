import errno
from time import sleep

import json
import logging
import os
import re
import requests
from bs4 import BeautifulSoup
from const import *


OUTPUT_DIR = 'comments'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def get_reviews_filename(product_id):
    filename = os.path.join(OUTPUT_DIR, '{}.json'.format(product_id))
    exist = os.path.isfile(filename)
    return filename, exist


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def persist_comment_to_disk(reviews):
    if len(reviews) == 0:
        return False
    product_id_set = set([r['product_id'] for r in reviews])
    assert len(product_id_set) == 1, 'all product ids should be the same in the reviews list.'
    product_id = next(iter(product_id_set))
    output_filename, exist = get_reviews_filename(product_id)
    dir_exist = os.path.exists('./' + OUTPUT_DIR)
    if not dir_exist:
        mkdir_p(OUTPUT_DIR)
    if reviews is not None:
        if not exist:
            with open(output_filename, 'w', encoding='utf-8') as fp:
                json.dump(reviews, fp, sort_keys=True, indent=4, ensure_ascii=False)
        else:
            f = open(output_filename, encoding='utf-8')
            text = json.load(f)
            for item in reviews:
                text.append(item)
            f.close()
            with open(output_filename, 'w+', encoding='utf-8') as fp:
                json.dump(text, fp, sort_keys=True, indent=4, ensure_ascii=False)
        return True


def extract_product_id(link_from_main_page):
    # e.g. B01H8A7Q42
    p_id = -1
    tags = ['/dp/', '/gp/product/']
    for tag in tags:
        try:
            p_id = link_from_main_page[link_from_main_page.index(tag) + len(tag):].split('/')[0]
        except:
            pass
    m = re.match('[A-Z0-9]{10}', p_id)
    if m:
        return m.group()
    else:
        return None


def get_soup(AMAZON_BASE_URL, url):
    temp = 0
    if AMAZON_BASE_URL not in url:
        url = AMAZON_BASE_URL + url
    nap_time_sec = 1
    logging.debug('Script is going to sleep for {} (Amazon throttling). ZZZzzzZZZzz.'.format(nap_time_sec))
    sleep(nap_time_sec)
    User_Agent = Agent_header[temp]
    header = {
        'User-Agent': User_Agent
    }
    logging.debug('-> to Amazon : {}'.format(url))
    out = requests.get(url, headers=header)
    assert out.status_code == 200
    soup = BeautifulSoup(out.content, 'lxml')
    while 'captcha' in str(soup):
        temp += 1
        sleep(nap_time_sec)
        User_Agent = Agent_header[temp]
        header = {
            'User-Agent': User_Agent
        }
        logging.debug('-> to Amazon : {}'.format(url))
        out = requests.get(url, headers=header)
        assert out.status_code == 200
        soup = BeautifulSoup(out.content, 'lxml')
        if (temp == 17):
            logging.info("ip banned")
            break
    return soup
