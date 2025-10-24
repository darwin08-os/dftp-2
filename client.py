#libs
import helper
import socket
import os

#vars
host = input("server ip : ")
port = 41000

print("trying to connect to : ",host)

#socket
client = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

data = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

print("trying to connect to :",host)

#connect
client.connect((host,port))
data.connect((host,41001))


print("connected successfully")
while True:
	try:
		command = input(f"{os.getcwd()}>")
		if command.startswith("!"): #general commands
			output = helper.ExecuteCommand(command[1:])
			print(output)

		if command[0:4]!='send'\
and command[0:3]!='get' and (command.startswith("cd") \
or command in ("ls","pwd")) :
			client.send(command.encode())
			size = str(client.recv(1024).decode())  # size of output in bytes
			print(size)
			if size.split("|")[0] == "check":
				size = int(size.split("|")[1])
			received = 0
			output_bytes = b""

			while received < size:
				chunk = data.recv(min(4096, size - received))  # read in 4 KB chunks
				if not chunk:
					break  # connection closed unexpectedly
				output_bytes += chunk
				received += len(chunk)

			output = output_bytes.decode(errors="replace")  # decode once at the end
			print(output)

		if command.startswith('send'):
			#three way handshake
			client.send(command.encode())
			if client.recv(1024).decode() == "READY":
				output = helper.SendData\
(client,command[5:],data)
			print(output)
		if command.startswith("get"):
			client.send(command.encode())
			if client.recv(1024).decode() == "send":
				client.send("READY".encode())
				output = helper.ReciveData(client,data)
				print(output)
	except KeyboardInterrupt:
		client.close()
		break
	except Exception as e:
		print("error :",e)


