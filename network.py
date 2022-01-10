import socket
from _thread import *

class Network:
	def __init__(self):
		self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server=""
		self.port=5555
		self.addr=(self.server,self.port)
		self.pos=self.connect()
		self.latestMov=""
	def getPos(self):
		return self.pos

	def connect(self):
		try:
			self.client.connect(self.addr)
			#return self.client.recv(2048).decode()
			start_new_thread(self.rec,(1,))
		except:
			print("FATAL ERROR")

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			# self.latestMov=self.client.recv(2048).decode()
		except socket.error as e:
			print("Socket Errror: ",str(e))
		except:
			print("SOME OTHER ERROR")

	def rec(self,a):
		tempRecv=""
		while True:
			try:
				tempRecv=self.client.recv(2048).decode()
			except:
				break
			if len(tempRecv)>0:
				self.latestMov=tempRecv
			print("RECEIVED MSG",tempRecv)

	def reset(self):
		self.latestMov=""
