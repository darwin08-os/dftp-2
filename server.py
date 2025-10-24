#important libraris
import helper
import socket

#variables
host = "0.0.0.0"
port = 41000

#socket
server = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

data_socket = socket.socket(socket.AF_INET,socket.\
SOCK_STREAM)

#bind host and port
server.bind((host,port))
data_socket.bind((host,41001))

#start listening
server.listen(10)
print("listening on : ",host)
print("started listening..")
data_socket.listen(10)
#recive connection
conn,addr = server.accept()
data_socket_conn,addr = data_socket.accept()
print(f"Client : {addr} ")

#remember : byte => str => int
while conn:
	try:
		data = conn.recv(1024).decode()
		if not data :
			break
		command = str(data)
		if command.startswith("cd") or command in ('ls', 'pwd'):
			try:
				output = helper.ExecuteCommand(command)	
				print(output)
			except Exception as e:
				output = f"ERROR: {e}"

			# Convert output to bytes for reliable sending
			output_bytes = output.encode(errors="replace")
			size = len(output_bytes)

			# First, send the size of output
			conn.send(str(f"check|{size}").encode())

			# Send the output in chunks
			chunk_size = 4096  # 4 KB per chunk
			sent = 0
			while sent < size:
				end = min(sent + chunk_size, size)
				data_socket_conn.send(output_bytes[sent:end])
				sent = end

					
		if command[0:4].lower() == 'send':
			conn.send("READY".encode())
			output = helper.ReciveData(conn,data_socket_conn)
			print(output)
		if command[0:3] == 'get':
			conn.send("send".encode())
			if conn.recv(1024).decode() == "READY":
				output = helper.SendData(conn,command[4:],data_socket_conn)
				print(output)
	except Exception as e :
		print(e)
	finally:
		server.close()
		




