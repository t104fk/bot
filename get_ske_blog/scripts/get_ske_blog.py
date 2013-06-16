#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import os
import smtplib
import difflib
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.Utils import formatdate
from email import Charset

# parameter
base_url = 'http://www2.ske48.co.jp/blog_pc/detail/?writer='
file_home = "your log directory"
save_path = file_home + "/%s"
local_file = file_home + "/content_"
GMAIL_ADDRESS = 'youraddress'
GMAIL_PASS = 'yourpassword'

def paramchk(argvs):
    if (len(argvs) != 3):
        print 'USAGE : ' + argvs[0] + ' "member" "youraddress"'
        sys.exit()

def get_title(src):
    pattern = re.compile(r'<h3>(.+?)</h3>')
    h3_list = []
    for match in pattern.finditer(src):
        h3 = match.group(1)
        h3_list.append(h3)
    h3_len = len(h3_list)
    if h3_len == 9:
        return h3_list[1]
    else:
        print 'h3 list len is changed! len is ' + str(h3_len)
        sys.exit()

def get_img_url(src):
    img = ''
    pattern = re.compile(r'url\((.+?)\)')
    for match in pattern.finditer(src):
        img = match.group(1)
        if img:
            return img

def download(url):
    req = urllib2.urlopen(url)
    output = save_path % os.path.basename(url)
    print output
    if not os.path.exists(output):
        file = open(output, 'wb')
        file.write(req.read())
        file.close()
    return output

def get_content(src):
    pattern = re.compile(r'</p><br />(.+?)</div>')
    for match in pattern.finditer(src):
        if match:
            return match.group(1)

def textchk(content, writer):
    local = open(local_file + writer + ".txt", "r") .read()
    if local.replace("\n", '') == content.replace("\n", ''):
        print 'blog text is already exists.'
        sys.exit()
    else:
        print '[update blog]' + writer

# -----mail start-----
# encode header Quoted-Printable and body base64
Charset.add_charset('shift_jis', Charset.QP, Charset.BASE64, 'shift_jis')
# use cp932 not shift_jis to convert encoding
Charset.add_codec('shift_jis', 'cp932')

def send(from_addr, to_addr, subject, body, img_path, encoding):
    #msg = MIMEText(body, 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    # attach img
    related = MIMEMultipart('related')
    alt = MIMEMultipart('alternative')
    related.attach(alt)

    content = MIMEText(body, 'plain', encoding)
    alt.attach(content)

    for filename in [img_path]:
        fp = file('%s' % filename, 'rb')
        img = MIMEImage(fp.read(), 'jpg', name=filename)
        related.attach(img)

        msg.attach(related)
        pass

    # if omit parameter, apply "localhost:25"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(GMAIL_ADDRESS, GMAIL_PASS)
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()
# -----mail end-----

def main(argvs):
    paramchk(argvs)
    writer = argvs[1]
    blog_src = str(urllib2.urlopen(base_url + writer).read())
    title = get_title(blog_src)
    img_url = get_img_url(blog_src)
    img_path = download(img_url)
    content = get_content(blog_src).replace("<br />", "\n")
    textchk(content, writer)
    # TODO : parameterize to address
    send(GMAIL_ADDRESS, argvs[2], title, content, img_path, 'utf-8')

if __name__ == "__main__":
    import sys
    main(sys.argv)
