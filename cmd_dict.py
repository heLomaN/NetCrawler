#!/usr/bin/env python
# coding=utf-8
import requests as rq
from BeautifulSoup import BeautifulSoup as bs

def query(word):
    query_dict = {'le':'eng', 'q':word}
    r = rq.get('http://dict.youdao.com/search', query_dict)

    soup = bs(r.text)
    trans_div = soup.find('div', {'class':'trans-container'})
    
    #print trans_div
    interpretations = trans_div.findAll('li')
    for elem in interpretations:
        print elem.string


if __name__ == '__main__':
    word = raw_input('Query:\t')
    print word
    while(word != 'q'):
        query(word)
        word = raw_input('Query:\t')

