import json
from const import *
from core_utils import *
from core_extract_comments import *
f = open("comments/B07NZP9YQF.json")
s = json.load(f)
print(len(s))
print(len(Agent_header))
AMAZON_BASE_URL = 'https://www.amazon.es'
product_id = 'B07WK57MJ2'
product_reviews_link = get_product_reviews_url(AMAZON_BASE_URL, product_id)
print (product_reviews_link)
so = get_soup(AMAZON_BASE_URL, product_reviews_link)
max_review_number = so.find(attrs={'data-hook': 'cr-filter-info-review-count'})
max_review_number = max_review_number.text.replace(u'\xa0', u' ').encode('utf-8')
max_review_number = str(max_review_number)
dt = max_review_number.split(' ')
for i in dt:
    if i.isdigit():
        max_review_number = int(i)
        break
#max_review_number = int(max_review_number)
print(max_review_number)