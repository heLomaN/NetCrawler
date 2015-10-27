#!/usr/bin/env python
# coding=utf-8
import requests as rq
import random as rd
from BeautifulSoup import BeautifulSoup as bs
from collections  import namedtuple
import datetime, time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

Topic = namedtuple('Topic', ['href', 'title', 'published_date', 'num_pages'])
HostName = "http://www.newsmth.net"

def extract_topic(text):
	soup = bs(text)
	topic_table = soup.find('table', {'class':'board-list tiz'})
	topics = topic_table.findAll('td', {'class':'title_9'})

	for elem in topics:
		#jump topped topics, eg. <tr class="top"></tr>
		if elem.parent.get('class', None) == 'top':
			continue
	
		a = elem.find('a')
		
		href = a['href']
		title = a.string
		
		num_pages = 1
		if (elem.span):
			other_pages = elem.span.findAll('a')
			num_pages += len(other_pages)
		
		published_date = elem.nextSibling.string
		try:
			timeArray = time.strptime(published_date, "%Y-%m-%d")
		except:
			today = datetime.date.today()
			published_date = today.__str__()
		
		yield Topic(href, title, published_date, num_pages)


def topics_first_n_page(n):
	topics = []

	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
	}

	query_dict = {}

	url_head = HostName + '/nForum/'
	r = rq.get(url_head, params = query_dict)


	r.encoding = 'gbk'

	url_head = HostName + '/nForum/board/WorkLife?ajax'
	
	headers = {
	'Host': 'www.newsmth.net',
	'Connection': 'keep-alive',
	'Accept': '*/*',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
	'Referer': 'http://www.newsmth.net/nForum/',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}

	cookies = r.cookies
	
	for page_idx in range(1, n + 1):
		query_dict = {'ajax': None, 'p': page_idx}
		
		r = rq.get(url_head, params = query_dict, headers = headers, cookies = cookies)

		r.encoding = 'gbk'
		
		topic_generator = extract_topic(r.text)
		for topic in topic_generator:
			topics.append(topic)
		
		print 'Pages scaned: ', page_idx, '/', n
		
	return topics	
	

def render(render_path, topics):
	f = open(render_path, 'w')
	
	def topic_to_tr(topic):
		format_tr = '''
			<tr>
				<td><a href="%s">%s</a></td>
				<td>%s</td>
				<td>%s</td>
			</tr>'''
	
		topic = topic._replace(href = HostName + topic.href)
		
		return format_tr % topic
	
	def topic_tr_itr():
		for topic in topics:
			topic_tr = topic_to_tr(topic)
			yield topic_tr
			
	# for topic_string in topic_tr_itr():
		# f.write(topic_string)
	table_content = ''.join(topic_tr_itr())
	
	table_templete = '''
		<table cellpadding="0" cellspacing="0">
			<thead>
			<tr>
				<th>主题</th>
				<th>发帖时间</th>
				<th>回复页数</th>
			</tr>
			</thead>
			<tbody>%s</tbody>
		</table>'''
	table_page = table_templete % table_content
	
	page_templete = '''
		<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.0 Transitional//EN'>
		<html>
		<head>
			<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
			<base target = "_blank">
			<link rel="stylesheet" type="text/css" href="style.css" >
		</head>
		<body>
		%s
		</body>
		</html>'''
	page = page_templete % table_page
	
	f.write(page)
		
	f.close()


if __name__ == "__main__":
	topics = topics_first_n_page(10)
	
	# sort by num_pages
	topics.sort(key = lambda topic: topic.num_pages, reverse = True)
	
	# delete which num_pages <= 1
	topics = filter(lambda topic: topic.num_pages >= 2, topics)
	
	render_path = 'worklife.html'
	render(render_path, topics)
