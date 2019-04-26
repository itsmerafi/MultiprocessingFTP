#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 7 - server_twisted.py
# Using Twisted to serve Launcelot users.
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor
from server_simple import server_loop
import socket, sys, json, glob, os
import launcelot

def recvall(sock, length):
	data = ''
	while len(data) < length:
		more = sock.recv(length - len(data))
		if not more:
			raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
		data += more
	return data

class Launcelot(Protocol):
	
	def connectionMade(self):
		print self
		self.question = ''
	def dataReceived(self, data):
		print data
		print 'Client:', repr(data)
		data = json.loads(data)
		if data.has_key('cmd'):
			if data['cmd']=='LS':
				if data['arg'] == "*" :
					res = glob.glob(data['arg'])
					res = "\n".join(res)
				else :
					if os.path.isdir(data['arg']):
						res = os.listdir(data['arg'])
						res = "\n".join(res)
					else:
						res = "Server : That is Not a Directory"
				print " <Send List> "
				
				self.transport.writeSequence(str(res))
			elif data['cmd']=='GET':
				filepath = "server/"+data['arg']
				print "Filepath : " + filepath
				if os.path.exists(filepath):
					data_send = []
					
					read = open(filepath,'rb').read() #readfile
					send_file = len(read) #size file
					 # send size file
					print "File Size Sending : ", send_file 
					 # send file
					print ' <Success!> '
					data_send.append('Download was successful')
					js = {'Preparing':'Preparing a file', 
					'size': str(send_file), 'read' : read, 
					'status' :'sukses'}
					js2 = json.dumps(js)
					self.transport.write(js2)
				else :
					js = {'Preparing':'Sorry, File not available'}
					js2 = json.dumps(js)
					self.transport.write(js2)

			elif data['cmd'] == 'PUT':
				filename = data['arg']
		            
				size = data['size'] #get size
				print "File Size Upload : ", size + "bit"
				#read = recvall(self, int(size)) #get file
				f = open("server/" + filename, 'wb+')
				f.write(data['read'])
				f.close()
				print ' <Success!> '
				self.transport.write('Successfully uploaded file')
			elif data['cmd'] == 'QUIT':
				print 'Process' 
				self.transport.write('Disconnecting..')
				print self , ' Disconnect..'
		            
		
factory = ServerFactory()
factory.protocol = Launcelot
reactor.listenTCP(1060, factory)
reactor.run()
