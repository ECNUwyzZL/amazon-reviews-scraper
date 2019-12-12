import json
from const import *
from core_utils import *
from core_extract_comments import *
from mail import *
# review =                               {'title': '123',
#                                         'rating': '2',
#                                         'body': 'fuck',
#                                         'product_id': '222',
#                                         'author_url': 'www.baidu.com',
#                                         'review_url': 'www.baidu.com',
#                                         'review_date': '123',
#                                         }
# send(review)
# /*
# f = open("comments/B07NZP9YQF.json")
# s = json.load(f)
# print(len(s))
# print(len(Agent_header))
AMAZON_BASE_URL = 'https://www.amazon.com'
# product_id = 'B07WK57MJ2'
# product_reviews_link = get_product_reviews_url(AMAZON_BASE_URL, product_id)
# print (product_reviews_link)
url = AMAZON_BASE_URL + '/gp/profile/amzn1.account.AFAFTNZFAFBE57FQF3E6TUQZZETQ/ref=cm_cr_arp_d_gw_btm?ie=UTF8'
res = requests.get(url, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60')
print(res)
so = BeautifulSoup(res.content, 'lxml')
author = so.find(attrs={'class':'a-size-extra-large'})
author_name = author.text
# max_review_number = so.find(attrs={'data-hook': 'cr-filter-info-review-count'})
# max_review_number = max_review_number.text.replace(u'\xa0', u' ').encode('utf-8')
# max_review_number = str(max_review_number)
# dt = max_review_number.split(' ')
# for i in dt:
#     if i.isdigit():
#         max_review_number = int(i)
#         break
# #max_review_number = int(max_review_number)
# print(max_review_number)