#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 7 - server_simple.py
# Simple server that only serves one client at a time; others have to wait.
import launcelot
import socket, sys, json, glob, os
def recvall(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
        data += more
    return data

def handle_client(sc):
	try:

		print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
		print sc
		while True:
		    message = sc.recv(1024)
		    print 'Client:', repr(message)
		    message = json.loads(message)
		    if message.has_key('cmd'):
		        if message['cmd']=='LS':
		            if message['arg'] == "*" :
		                res = glob.glob(message['arg'])
		                res = "\n".join(res)
		            else:
		                if os.path.isdir(message['arg']):
		                    res = os.listdir(message['arg'])
		                    res = "\n".join(res)
		                else :
		                    res = "Server : That is Not a Directory"

		            print " <Send List> "
		            sc.sendall(res)

		        elif message['cmd']=='GET':
		           
		            filepath = "server/"+message['arg']
		            print "Filepath : " + filepath
		            if os.path.exists(filepath):
		                sc.sendall('Preparing a file')
		                read = open(filepath,'rb').read() #readfile
		                send_file = len(read) #size file
		                sc.sendall(str(send_file)) # send size file
		                print "File Size Sending : ", send_file 
		                sc.sendall(read) # send file
		                print ' <Success!> '
		                sc.sendall('Download was successful')
		            else :
		                sc.sendall('Sorry, File not available')
		                

		        elif message['cmd'] == 'PUT':
		            filename = message['arg']
		            
		            size = sc.recv(2048) #get size
		            print "File Size Upload : ", size + "bit"
		            read = recvall(sc, int(size)) #get file

		            f = open("server/" + filename, 'wb+')
		            f.write(read)
		            f.close()

		            print ' <Success!> '
		            sc.sendall('Successfully uploaded file')
		        elif message['cmd'] == 'QUIT':
		            print 'Process' 
		            sc.sendall('Disconnecting..')
		            print 'Close connection..'
		            sc.close()
		            exit(1)
		            
		    else:
		        sc.sendall('invalid command...')
	except EOFError:
		sc.close()
def server_loop(listen_sock):
	while True:
		sc, sockname = listen_sock.accept()
		handle_client(sc)

if __name__ == '__main__':
	listen_sock = launcelot.setup()
	server_loop(listen_sock)