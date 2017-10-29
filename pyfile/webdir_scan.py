#!/usr/bin/env python

import re
import sys
import requests
import threading
import argparse
from multiprocessing.dummy import Pool

TOTAL = 0
COUNT = 0
WIDTH = 50
	
headers = {
	'Accept': '*/*',
	'Referer': 'https://www.baidu.com',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Cache-Control': 'no-cache',
}

class Finished(Exception):
	pass


def send_request(url):
	global COUNT
	r = requests.get(url,headers = headers, allow_redirects = False,timeout = 20)
	notfoundpagetext = requests.get(url + '/notexitstktdhhhhhh',allow_redirects = False).text
	if r.status_code == 200 and r.text != notfoundpagetext:
		COUNT+=1


OUTPUT_LOCK = threading.Lock()
def progress_bar():
	OUTPUT_LOCK.acquire()
	sys.stdout.write('\r\033[K')
	finished = COUNT*100/TOTAL
	finished_width = COUNT * WIDTH / TOTAL
	unfinished_width = WIDTH - finished_width
	sys.stdout.write(str(finished)+"%" + '[' \
			+ ' \033[32m=\033[0m' * (finished_width) \
			+ " \033[32m=\033[0m" \
			+ '\033[32m=\033[0m' * unfinished_width + ']')
	sys.stdout.flush()
	OUTPUT_LOCK.release()

def main():
	parser = argparse.ArgumentParser('the web scan start')
	parser.add_argument("-u", "--url", type = str)
	arg = parser.parse_args()
	url = arg.url
	r = send_request(url)
	
	urls = []
	global TOTAL
	with open('dict.txt', 'r') as infile:
			line = infile.readline().strip('\r\n')
			while(line):
				if line[0:1]!='#':
					urls.append(url+line)
					TOTAL+=1
				line = infile.readline().strip('\r\n')

	try:
		pool = Pool(100)
		pool.map(send_request, [url for url in urls])
		progress_bar()
	except KeyboardInterrupt:
		pool.terminate()
	except ZeroDivisionError:
		pool.terminate()
	except Finished:
		pool.terminate()

	print 'scan end'

if __name__ == '__main__':
	main()
