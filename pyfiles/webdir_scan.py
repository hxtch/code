#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import requests
import threading
import argparse
from multiprocessing.dummy import Pool


TOTAL = 0
COUNT = 1
WIDTH = 60
OUTPUT_LOCK = threading.Lock()

headers = {
	'Accept': '*/*',
	'Referer': 'https://www.baidu.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Cache-Control': 'no-cache',
}

f = open('effienturl2.txt','wb')

def progress_bar():
	OUTPUT_LOCK.acquire()
	sys.stdout.write('\r\033[K')
	finished = COUNT * 100 / TOTAL
	finished_width = COUNT * WIDTH / TOTAL
	unfinished_width = WIDTH - finished_width
	sys.stdout.write(str(finished)+"%" + '[' \
			+ '\033[32m=\033[0m' * (finished_width) \
			+ "\033[32m>\033[0m"  \
			+ '\033[31m=\033[0m' * unfinished_width + ']')
	sys.stdout.flush()
	OUTPUT_LOCK.release()

def open_dict(url):
	global TOTAL
	urls = []
	with open('dict.txt', 'r') as f:
			for eachline in f.readlines():
				eachline = eachline.strip('\r\n')
				if eachline[0:1]!='#':
					urls.append(url+eachline)
					TOTAL+=1

	return urls
	

def send_request(url):
	global COUNT
	r = requests.get(url,headers = headers, allow_redirects = False,timeout = 60)
	COUNT += 1
	notfoundpagetext = requests.get(url + '/notexitstktdhhhhhh',allow_redirects = False).text
	if r.status_code == 200 and r.text != notfoundpagetext:
#		print "%d %s\n"%(COUNT, url)
		f.write(url)
		f.write('\n')
	if (COUNT % (TOTAL / WIDTH) == 0) :	
		progress_bar()

def main():
	parser = argparse.ArgumentParser(description = 'the web scan start')
	parser.add_argument("-u", "--url", type = str)
	arg = parser.parse_args()
	url = arg.url
	urls = open_dict(url)
	try:
		pool = Pool(1000) #创建拥有50个进程数量的进程池
		pool.map_async(send_request, [eurl for eurl in urls])
		pool.close() #关闭进程池，不再接受新的进程
		pool.join() #主进程阻塞，等待子进程的退出
	except KeyboardInterrupt:
		pool.terminate()

	f.close()
	print 'scan end'

if __name__ == '__main__':
	main()
