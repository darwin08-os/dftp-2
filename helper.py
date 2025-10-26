#libs
import subprocess
import os
import traceback
from tqdm import tqdm

def filterCommand(command):
        if command == "ls":
                return "dir"
        else: 
                if command == "pwd":
                        return "cd"
        if command == "cd":
                return "cd"
        if command.startswith("cd") and len(command)>2:
                os.chdir(command[3:].strip())
                return "cd"
        

def ExecuteCommand(command):
        command_to_run = filterCommand(command)
        
        run = subprocess.Popen(command_to_run,shell=True\
,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        output = run.stdout.read() + run.stderr.read()

        return output


def SendData(c,filepath,data):
        try:
                if "/" not in filepath and \
"\\" not in filepath:
                        filepath = os.path.join(\
os.getcwd(),os.path.basename(filepath.strip()))
                        #print(filepath)

                #file size and name
                filename = filepath.replace("\\","/")\
.split("/")[-1]

                filesize = str(os.path.getsize(filepath))

                #send filename and filesize
                header = f"{filename}|{filesize}"
                c.sendall(header.encode())
                #c.sendall(filename.encode())
                #c.sendall(filesize.encode())
                filesize = int(filesize)
                with open(filepath,"rb") as f :
                        pbar = tqdm(total=max(filesize,4096),\
unit='B',unit_scale=True,desc="Uploading the file")
                        while True:
                                content = f.read(4096)
                                if not content:
                                        break
                                data.sendall(content)
                                pbar.update(len(content))
                        pbar.close()
                return "Done from our/theirSide"

        except Exception as e:
                return e

cwd = os.getcwd()
def ReciveData(c,reciever):
        try:
                header = c.recv(1024).decode()
                filename = header.split("|")[0]
                filesize = int(header.split("|")[1])
                print(filename)
                print(filesize)
                remain = filesize
                with open(filename,"wb") as f :
                        pbar = tqdm(total=max(filesize,4096),\
unit='B',unit_scale=True,desc="Uploading the file")
                        while remain > 0:
                                if filesize >= 4096:
                                        chunk = 4096
                                else:
                                        chunk = remain
                                content = reciever.recv(chunk)
                                if not content:
                                        break
                                f.write(content)
                                remain = remain - len(content)
                                pbar.update(len(content))
                        pbar.close()
                return "recieved"
        except Exception as e :
                print(traceback.format_exc())
                return e		

def handle_client(server,conn,data_socket_conn,running):
        while running:
                try:
                        data = conn.recv(1024).decode()
                        if not data :
                                break
                        command = str(data)
                        if command.startswith("cd") or command in ('ls', 'pwd'):
                                try:
                                        output = ExecuteCommand(command)	
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
                                output = ReciveData(conn,data_socket_conn)
                                print(output)
                        if command[0:3] == 'get':
                                conn.send("send".encode())
                                if conn.recv(1024).decode() == "READY":
                                        output = SendData(conn,command[4:],data_socket_conn)
                                        print(output)
                except Exception as e :
                        print(e)
                        conn.close()
                        data_socket_conn.close()
