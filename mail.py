import smtplib
from email.mime.text import MIMEText
from email.header import Header
from const import *

from_addr = MAIL_FROM
password = MAIL_PASSWORD
to_addr = MAIL_TO
smtp_server = MAIL_SERVER

def structure(review):
    title = review['product_id'] + u"---差评" + "    " + review['title']
    content = u'<div><p style="overflow-wrap: break-word;margin: 5px 0px; font-family: &quot;sans serif&quot;, tahoma, verdana, helvetica; font-size: 12px;"><span style="font-size: 18px;"><strong><span style="font-size: 32px;">注意</span></strong><span style="font-size: 32px;"><strong>​!</strong></span></span></p><p style="overflow-wrap: break-word; margin: 5px 0px; font-family: &quot;sans serif&quot;, tahoma, verdana, helvetica; font-size: 12px;"><span style="font-size: 18px;"><span style="font-size: 32px;"><strong><span style="font-size: 10px;">​<span style="font-size: 14px;">​又出现了新的差评，具体信息如下：</span></span><br></strong></span></span></p><p style="overflow-wrap: break-word; margin: 5px 0px; font-family: &quot;sans serif&quot;, tahoma, verdana, helvetica; font-size: 12px;"></p><ul><li><span style="font-size: 18px;"><span style="font-size: 32px;"><strong><span style="font-size: 10px;"><span style="font-size: 14px;">​星级：' + review['rating'] + u'</span></span></strong></span></span></li><li><b>姓名：' + review['author_name'] + u'</b></li><li><b>客户链接：<a href="' + review['author_url'] + '">' + review['author_url'] + u'</a></b></li><li><b>差评内容：' + review['body'] + u'</b></li><li><b>链接：<a href="' + review['review_url'] + '">' + review['review_url'] + u'</a></b></li></ul><p></p></div><div><includetail><!--<![endif]--></includetail></div>'
    return title, content
def send(review):
    try:
        title, content = structure(review)
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(title)
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Error %s" % e)


