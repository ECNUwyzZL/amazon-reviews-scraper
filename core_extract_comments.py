import logging
import math
import re
import textwrap
import os
import json
from mail import send

from core_utils import *


# https://www.amazon.co.jp/product-reviews/B00Z16VF3E/ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=1

def get_product_reviews_url(AMAZON_BASE_URL, item_id, page_number=None):
    if not page_number:
        page_number = 1
    return AMAZON_BASE_URL + '/product-reviews/{}/ref=' \
                             'cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews' \
                             '&showViewpoints=1&sortBy=recent&pageNumber={}'.format(
        item_id, page_number)


def get_comments_based_on_keyword(AMAZON_BASE_URL, search):
    logging.info('SEARCH = {}'.format(search))
    url = AMAZON_BASE_URL + '/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + \
          search + '&rh=i%3Aaps%2Ck%3A' + search
    soup = get_soup(AMAZON_BASE_URL, url)

    product_ids = [div.attrs['data-asin'] for div in soup.find_all('div') if 'data-index' in div.attrs]
    logging.info('Found {} items.'.format(len(product_ids)))
    for product_id in product_ids:
        logging.info('product_id is {}.'.format(product_id))
        reviews = get_comments_with_product_id(AMAZON_BASE_URL, product_id)
        logging.info('Fetched {} reviews.'.format(len(reviews)))
        persist_comment_to_disk(reviews)


def get_comments_with_product_id(AMAZON_BASE_URL, product_id):
    reviews = list()
    if product_id is None:
        return reviews
    if not re.match('^[A-Z0-9]{10}$', product_id):
        return reviews

    product_reviews_link = get_product_reviews_url(AMAZON_BASE_URL, product_id)
    so = get_soup(AMAZON_BASE_URL, product_reviews_link)
    max_review_number = so.find(attrs={'data-hook': 'cr-filter-info-review-count'})
    if max_review_number is None:
        return reviews
    max_review_number = max_review_number.text.replace(u'\xa0', u' ').encode('utf-8')
    max_review_number = str(max_review_number)
    dt = max_review_number.split(' ')
    for i in dt:
        if i.isdigit():
            max_review_number = int(i)
            break
    max_page_number = max_review_number * 0.1  # displaying 10 results per page. So if 663 results then ~66 pages.
    max_page_number = math.ceil(max_page_number)
    print(max_review_number, "\n")
    filename, is_exsits = get_reviews_filename(product_id)
    is_exsits = os.path.exists(filename)
    if is_exsits:
        li = list()
        f = open(filename, encoding='utf-8')
        text = json.load(f)
        f.close()
        number = len(text)
        print(number)
        if number < max_review_number:
            for item in text:
                li.append(item['review_url'])
            hashlist = set(li)
            now_page = math.ceil(number * 0.1)
            for page_number in range(now_page, max_page_number):
                page_number = max_page_number - page_number + 1
                if page_number > 1:
                    product_reviews_link = get_product_reviews_url(AMAZON_BASE_URL, product_id, page_number)
                    so = get_soup(AMAZON_BASE_URL, product_reviews_link)

                cr_review_list_so = so.find(id='cm_cr-review_list')

                if cr_review_list_so is None:
                    logging.info('No reviews for this item.')
                    break

                reviews_list = cr_review_list_so.find_all('div', {'data-hook': 'review'})

                if len(reviews_list) == 0:
                    logging.info('No more reviews to unstack.')
                    break

                for review in reviews_list:
                    review_url = review.find(attrs={'data-hook': 'review-title'}).attrs['href']
                    if review_url in hashlist:
                        continue
                    else:
                        rating = review.find(attrs={'data-hook': 'review-star-rating'}).attrs['class'][2].split('-')[
                            -1].strip()
                        body = review.find(attrs={'data-hook': 'review-body'}).text.strip()
                        title = review.find(attrs={'data-hook': 'review-title'}).text.strip()
                        author_url = review.find(attrs={'data-hook': 'genome-widget'}).find('a', href=True)
                        review_date = review.find(attrs={'data-hook': 'review-date'}).text.strip()
                        author_name = review.find(attrs={'data-hook': 'genome-widget'}).find(attrs={'class': 'a-profile-content'}).text
                        if author_url:
                            author_url = author_url['href'].strip()
                        try:
                            helpful = review.find(attrs={'data-hook': 'helpful-vote-statement'}).text.strip()
                            helpful = helpful.strip().split(' ')[0]
                        except:
                            # logging.warning('Could not find any helpful-vote-statement tag.')
                            helpful = ''
                        logging.info('***********************************************')
                        logging.info('TITLE    = ' + title)
                        logging.info('RATING   = ' + rating)
                        logging.info('CONTENT  = ' + '\n'.join(textwrap.wrap(body, 80)))
                        logging.info('HELPFUL  = ' + helpful)
                        logging.info('AUTHOR URL  = ' + author_url if author_url else '')
                        logging.info('REVIEW URL  = ' + review_url if review_url else '')
                        logging.info('REVIEW DATE  = ' + review_date if review_date else '')
                        logging.info('***********************************************\n')
                        review_text = ({'title': title,
                                        'rating': rating,
                                        'body': body,
                                        'product_id': product_id,
                                        'author_url': AMAZON_BASE_URL + author_url,
                                        'review_url': AMAZON_BASE_URL + review_url,
                                        'review_date': review_date,
                                        'author_name': author_name,
                                        })
                        reviews.append(review_text)
                        rating_war = int(rating)
                        if rating_war <= 3:
                            send(review_text)
        else:
            logging.info('no further reviews')
    else:
        for page_number in range(1, max_page_number + 1):
            if page_number > 1:
                product_reviews_link = get_product_reviews_url(AMAZON_BASE_URL, product_id, page_number)
                so = get_soup(AMAZON_BASE_URL, product_reviews_link)

            cr_review_list_so = so.find(id='cm_cr-review_list')

            if cr_review_list_so is None:
                logging.info('No reviews for this item.')
                break

            reviews_list = cr_review_list_so.find_all('div', {'data-hook': 'review'})

            if len(reviews_list) == 0:
                logging.info('No more reviews to unstack.')
                break

            for review in reviews_list:
                rating = review.find(attrs={'data-hook': 'review-star-rating'}).attrs['class'][2].split('-')[-1].strip()
                body = review.find(attrs={'data-hook': 'review-body'}).text.strip()
                title = review.find(attrs={'data-hook': 'review-title'}).text.strip()
                author_url = review.find(attrs={'data-hook': 'genome-widget'}).find('a', href=True)
                author_name = review.find(attrs={'data-hook': 'genome-widget'}).find(attrs={'class':'a-profile-content'}).text
                review_url = review.find(attrs={'data-hook': 'review-title'}).attrs['href']
                review_date = review.find(attrs={'data-hook': 'review-date'}).text.strip()
                if author_url:
                    author_url = author_url['href'].strip()
                try:
                    helpful = review.find(attrs={'data-hook': 'helpful-vote-statement'}).text.strip()
                    helpful = helpful.strip().split(' ')[0]
                except:
                    # logging.warning('Could not find any helpful-vote-statement tag.')
                    helpful = ''

                logging.info('***********************************************')
                logging.info('TITLE    = ' + title)
                logging.info('RATING   = ' + rating)
                logging.info('CONTENT  = ' + '\n'.join(textwrap.wrap(body, 80)))
                logging.info('HELPFUL  = ' + helpful)
                logging.info('AUTHOR URL  = ' + author_url if author_url else '')
                logging.info('REVIEW URL  = ' + review_url if review_url else '')
                logging.info('REVIEW DATE  = ' + review_date if review_date else '')
                logging.info('***********************************************\n')
                review_text = ({'title': title,
                                'rating': rating,
                                'body': body,
                                'product_id': product_id,
                                'author_url': AMAZON_BASE_URL + author_url,
                                'review_url': AMAZON_BASE_URL + review_url,
                                'review_date': review_date,
                                'author_name': author_name,
                                })
                reviews.append(review_text)
                rating_war = int(rating)
                if rating_war <= 3:
                    send(review_text)
    return reviews


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    _reviews = get_comments_with_product_id('https://www.amazon.com', 'B00BV0W8RQ')
    print(_reviews)
    persist_comment_to_disk(_reviews)
