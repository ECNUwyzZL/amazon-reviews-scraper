import argparse

from core_extract_comments import *
from core_utils import *


def run(search, input_product_ids_filename):
    product_ids = list()
    if input_product_ids_filename is not None:
        with open(input_product_ids_filename, 'r') as r:
            for p in r.readlines():
                pro_obj = p.strip('\n').split(' ')
                #print(pro_obj)
                product_ids.append(pro_obj)
            logging.info('{} product ids were found.'.format(len(product_ids)))
            reviews_counter = 0
            for product_id in product_ids:
                reviews = get_comments_with_product_id(product_id[1],product_id[0])
                reviews_counter += len(reviews)
                logging.info('{} reviews found so far.'.format(reviews_counter))
                if reviews is not None:
                    persist_comment_to_disk(reviews)
    else:
        default_search = 'iPhone'
        search = default_search if search is None else search
        reviews = get_comments_based_on_keyword('https://www.amazon.com', search)
        persist_comment_to_disk(reviews)


def get_script_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    input_product_ids_filename = args.input
    search = args.search
    return search, input_product_ids_filename


def main():
    search, input_product_ids_filename = get_script_arguments()
    run(search, input_product_ids_filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
