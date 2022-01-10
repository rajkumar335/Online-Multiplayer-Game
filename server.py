import socket
from _thread import *

server=""
port=5555
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	s.bind((server,port))

except socket.error as e:
	print(str(e))

except:
	print("SOME ERROR OCCURED WHILE BINDING THE SOCKET TO SERVER AND THE PORT")
s.listen(2)
print("Server started! Waiting for a connection....")

pos=[(0,0,3),(100,100,4)]

def threaded_client(conn):
	reply=""
	global Conn
	while True:
		try:
			data=readPos(conn.recv(2048).decode("utf-8"))
			pos[data[2]-1]=data


			if not data:
				print("Server Disconned!")
				break
			else:
				if data[2]==1:
					reply=pos[0]
				else:
					reply=pos[1]
				print("Received msg: ",data)

			for c in Conn:
				print("Sending: ",reply,"to:",c)
				c.send(str.encode(makePos(reply)))
		except Exception as e:
				print(e)
				break
	print("Connection Terminated!")
	conn.close()
	Conn.remove(conn)

def readPos(posn):
	posn=posn.split(",")
	return int(posn[0]),int(posn[1]),int(posn[2])

def makePos(posn):
	return str(posn[0])+","+str(posn[1])+","+str(posn[2])

Conn=[]
Addr=[]

while True:
	conn, addr =s.accept()
	Conn.append(conn)
	Addr.append(addr)
	print("Addr: ",Addr)
	print("Connected to: ",addr)
	start_new_thread(threaded_client,(conn,))
