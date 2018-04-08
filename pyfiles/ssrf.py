import requests
import re
import socket
from socket import inet_aton
from struct import unpack

# turning ip into int
def ip2long(ip_addr):
	return unpack("!L",inet_aton(ip_addr))[0]

# judging  whether ip is inner ip
def is_inner_address(ip_addr):


	pattern = re.compile('^(https?)://(((\d{1,3}\.){3}\d{1,3})|(.*))'
)
	schema = re.search(pattern, ip_addr).group(1)
	ip_addr = re.search(pattern, ip_addr).group(2)
	assert(schema, 'schema is wrong(must be http or https)')
	assert(ip_addr, 'ip format is wrong')

#get ip or domain
	ip_addr = socket.getaddrinfo(ip_addr, schema)[0][4][0]

	ip_addr = ip2long(ip_addr)
	
	
	if ip2long('127.0.0.1') <= ip_addr < ip2long('127.255.255.255'):
		return True
	elif ip2long('172.16.0.0') <= ip_addr < ip2long('172.31.255.255'):
		return True
	elif ip2long('10.0.0.0') <= ip_addr < ip2long('10.255.255.255'):
		return True
	elif ip2long('192.168.0.0') <= ip_addr < ip2long('192.168.255.255'):
		return True
	else:
	 	return False

def main():
	
	url = raw_input('input url:')
	
	try:
		if is_inner_address(url):
			raise Exception('hacker~')
		r = requests.get(url=url, allow_redirects=False)
		while r.is_redirect:
			url = r.headers['location']
			if is_inner_address(url):
				raise Exception('hacker~')
			r = requests.get(url = url, allow_redirects=False)
		
		print 'url is nomal url'
	
	except Exception,e:
		print e

if __name__ == '__main__':
	main()
