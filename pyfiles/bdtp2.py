# -*- coding: utf-8 -*-
#!/usr/bin/env python

import gevent
from gevent import monkey ; monkey.patch_all()
import re
import time
import os
import requests
import argparse
import sys

TOTAL = 0 #爬取总数
COUNT = 1 #爬取成功图片数

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

char_table = {ord(key):ord(value) for key, value in char_table.items()}
def decode(url):
	for key, value in str_table.items():
		url = url.replace(key, value)
	return url.translate(char_table)

def geturl(title,page,height = "", width = ""):
#此处的url是baidu图片的json接口
	url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=' + title.encode('utf-8') + '&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=' + title.encode('utf-8') + '&s=&se=&tab=&width=' + width + '&height=' + height + '&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn=' + page + '&rn=60&gsm=1e00000000001e&1490169411926='
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'Accept': 'text/plain, */*; q=0.01',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		"referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1490169358952_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=" + title.encode('utf-8')
		}
	page = requests.get(url, headers = headers, timeout = 10).content.decode('utf-8')
	pattern = re.compile('"objURL":"(.*?)"', re.S)
	imgUrls = re.findall(pattern, page)

	global TOTAL
	for i in imgUrls:
		TOTAL = TOTAL +1

	return imgUrls

#进度条的实现
def update_progress_bar():
	global COUNT
	WIDTH = ' ' * TOTAL
	sys.stdout.write('\r\033[K')
	finished = COUNT * 100 / TOTAL
	finished_width = COUNT
	unfinished_width = TOTAL - COUNT
	sys.stdout.write(str(finished) + '%' + '['
	+ '\033[32m=\033[0m' * (finished_width) 
	+ "\033[32m>\033[0m" 
	+ '\033[31m=\033[0m' * unfinished_width + ']' )
	sys.stdout.flush()
	COUNT = COUNT + 1

def getImg(imgurl, title):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	try:
		imgUrl = decode(imgurl)
		u = requests.get(imgUrl, headers = headers, timeout = 10)
		data = u.content
		f= open(title + '/' + title + str(time.time()) +'.jpg', 'wb')
		f.write(data)
		f.close()
		update_progress_bar()
	except:
		return False

def mkdir(path):
	path = path.strip()
	isExists = os.path.exists(path)
	if not isExists:
		os.makedirs(path)
	else:
		return False

def main():
	ts = []
	parser = argparse.ArgumentParser()
	parser.add_argument('-T', '--title', type = str)
	parser.add_argument('-P', '--page', type = int)
	parser.add_argument('-W', '--width', nargs = '?', default = "")
	parser.add_argument('-H', '--height', nargs = '?', default = "")
	arg = parser.parse_args()
	
	title = arg.title.decode(sys.stdin.encoding).replace(' ', '+')
	page = (arg.page - 1) * 60
	width = arg.width
	height = arg.height
	startTime = time.time()
	mkdir(title)
	imgUrls = geturl(title, str(page), width, height)
	
	try:
		for imgUrl in imgUrls:
			t = gevent.spawn(getImg, imgUrl, title)#创建协程
			ts.append(t)
		gevent.joinall(ts)
	except KeyboardInterrupt:
		pass

	print "\nTotal " + str(TOTAL) + " images, " + str(TOTAL-COUNT+1) + "images crawling failed"
	print "Time cost: "  + str(time.time() - startTime) + 's'

if __name__ == '__main__':
	main()
