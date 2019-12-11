import smtplib
from email.mime.text import MIMEText
from email.header import Header
from const import *

from_addr = MAIL_FROM
password = MAIL_PASSWORD
to_addr = MAIL_TO
smtp_server = MAIL_SERVER

def structure(review):
    title = review['product_id'] + "---bad comments" + "    " + review['title']
    content = "rate:" + review['rating']
    content += "comment:" + review['body'] + "\n" + "comment_url:" + review['review_url'] + "\n" + "date:" + review['review_date']
    return title, content
def send(review):
    try:
        title, content = structure(review)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(title)
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Error %s" % e)


