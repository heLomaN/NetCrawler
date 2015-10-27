#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests as rq
from BeautifulSoup import BeautifulSoup as bs

from collections  import namedtuple
Topic = namedtuple('Topic', ['href', 'title', 'published_date', 'num_pages'])

driver = webdriver.PhantomJS()


# with open('nga_hot.html', 'w') as f:
	# f.write(source_code.encode('utf-8'))
	# f.close()

# driver.get_screenshot_as_file('ajax.png')

# topicrows.screenshot('ajax_elem.png')

def extract_topic(source_code):
	soup = bs(source_code)
	topics = soup.findAll('td', {'class':'c2 posticon'})

	# print len(topics)
	for topic in topics:
		topic_as = topic.findAll('a', None)
		# for e in topic_as:
			# print e.attrs
			
		topic_as = filter(lambda x : x.get('class', 'not_a_topic_title').startswith('topic'), topic_as)

		topic_a = topic_as[0]
		href = topic_a['href']
		title = topic_a.text
		
		# calc published_date
		date_td = topic.findNextSibling('td', attrs = {'class': 'c3'})
		date_span = date_td.findAll('span', attrs = {'class': 'silver postdate'})[0]
		published_date = date_span.get('title')
		# print published_date
		# print date_td
		
		# calc number of pages
		num_pages = 1
		pages_span = topic.findAll('span', {'class':'pager'})
		if pages_span:
			heref_pages = pages_span[0].findAll('a')
			num_pages = int(heref_pages[-1].text)
			
		yield Topic(href, title, published_date, num_pages)

def topics_first_n_page(n):
	topics = []
	for page_idx in range(1, n + 1):
		url_head = 'http://bbs.ngacn.cc/thread.php'
		full_url = url_head + '?fid=-7&page=' + str(page_idx)

		topicrows_id = "topicrows"

		driver.get(full_url)
		WebDriverWait(driver, 10).until(
					lambda driver: driver.find_element_by_id(topicrows_id))

		topicrows = driver.find_element_by_id(topicrows_id)

		source_code = topicrows.get_attribute('innerHTML')
		
		topic_generator = extract_topic(source_code)
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
	
		# topic = topic._replace(href = topic.href)
		
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
	topics = topics_first_n_page(20)
	
	# sort by num_pages
	topics.sort(key = lambda topic: topic.num_pages, reverse = True)
	
	# delete which num_pages <= 1
	topics = filter(lambda topic: topic.num_pages >= 2, topics)
	
	render_path = 'nga_hot.html'
	render(render_path, topics)