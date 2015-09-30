#!/usr/bin/env python
# coding=utf-8
import requests as rq
import random as rd

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
'Host': 'bbs.ngacn.cc',
'Connection': 'keep-alive',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
'Referer': 'http://bbs.ngacn.cc/thread.php?fid=-7&page=1',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8'
#'Cookie': 'lastvisit=1444740559; ngaPassportUid=guest0561cfdcf63d5e; guestJs=1444740559',
}

page_idx = 1
query_dict = {'fid':-7, 'page':page_idx}

url_head = 'http://bbs.ngacn.cc/thread.php'
r = rq.get(url_head, params = query_dict)
#r = rq.get(url_head, params = query_dict, headers = headers)

print r.text


rand = rd.randint(1, 999)
query_dict = {'fid':-7, 'page':page_idx, 'rand': rand}
cookies = r.cookies
r = rq.get(url_head, params = query_dict, headers = headers, cookies = cookies)

print r.url
r.encoding = 'gbk'
#print r.text
f = open('test.html', 'w')
f.write(r.text)
f.close()

#print r.json()


