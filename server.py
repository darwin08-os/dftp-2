#important libraris
import helper
import socket
import threading
import time
import sys
#variables
host = "0.0.0.0"
port = 41000
running = True

#socket
server = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


data_socket = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)
data_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


client = socket.socket()
data_s = socket.socket()                                	
def handle_close():
	global running
	while True:
		ask = input("enter q for exit : ")
		if ask == "q":
			running = False
			client.connect(("127.0.0.1",41000))
			data_s.connect(("127.0.0.1",41001))
			time.sleep(1)
			break
		sys.exit(0)


#bind host and port
server.bind((host,port))
data_socket.bind((host,41001))

#start listening
server.listen(5)
print("listening on : ",host)
print("started listening..")
data_socket.listen(5)
#recive connection
t2 = threading.Thread(target=handle_close)
t2.start()
while running:
	conn,addr = server.accept()
	data_socket_conn,addr = data_socket.accept()
	t1 = threading.Thread(target=helper.handle_client,args=(server,conn,data_socket_conn,running),daemon=True)
	t1.start()
