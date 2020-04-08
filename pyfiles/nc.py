#!/usr/bin/env python

import sys
import argparse
import socket
import threading
import subprocess


listen 				= False
command 			= False
upload 				= False
execute 			= ""
target 				= ""
upload_destination 	= ""
port 				= 0

#创建tcp客户端
def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect((target, port))
		print "successful connect a server"
		if len(buffer):
			client.send(buffer)

		while True:
			recv_len = 1
			response = ""
			
			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				response += data

				if recv_len < 4096:
					break

			print response,

			buffer = raw_input("")
			buffer += '\n'

			client.send(buffer)

	except:
		print "[*]Exception Exiting."
		client.close()

#创建tcp服务器
def server_loop():
	global target
	
	if not len(target):
		target = "0.0.0.0"

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	server.listen(5)

	while True:
		print "Waiting for conection"
		client_socket, add = server.accept()
		client_thread = threading.Thread(target = client_handler, args = (client_socket,))
		client_thread.start()

def run_command(command):
	command = command.rstrip()

	try:
		output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
	except:
		output = "Failed to execute command.\n"
	
	return output

#处理客户端数据
def client_handler(client_socket):
	global upload
	global execute
	global command
	
#检测上传文件
	if len(upload_destination):
		file_buffer = ""
		
		while True:
			data = client_socket.recv(1024)
			
			if not data:
				break
			else:
				file_buffer += data

#接受数据并写出
		try:
			file_descriptior = open(upload_destination)
			file_descriptior.write(file_buffer)
			file_descriptior.close()
			client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
		except:
			client_socket.send("failed to save file to %s\r\n" % upload_destination)


	if len(execute):
		output = run_command(execute)
		client_socket.send(output)
	
	if command:
		while True:
			client_socket.send("<BHP:#> ")
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
				response = run_command(cmd_buffer)
	
				client_socket.send(response)

def main():
	global listen 			
	global command 			
	global port 			
	global execute 			
	global target 			
	global upload_destination


	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--host",type = str,nargs = '?', default = "", help = "target host")
	parser.add_argument("-p", "--port",type = int, nargs = 1, default = 0, help = "target port")
	parser.add_argument("-l", "--listen", action = 'store_true', help = "listen on [host]:[port] for incoming connections" )
	parser.add_argument("-e", "--execution", type = str, nargs = '?', default = "", help = "execute the given file upon receiving a connection")
	parser.add_argument("-c", "--command", action = 'store_true',help = "initialize a command shell")
	parser.add_argument("-u", "--upload",type = str,nargs = '?', default = upload_destination, help = "upon receiving connection upload a file and write to [destination]")
	args = parser.parse_args()
	
	execute = args.execution
	target = args.host
	port = args.port[0]
	listen = args.listen
	command = args.command
	upload_destination = args.upload
	
	if not listen and len(target) and port > 0:
		buffer = sys.stdin.read()
		client_sender(buffer)
	
	if listen:
		server_loop()

if __name__ == '__main__':
	main()
