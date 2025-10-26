# Python CLI FTP
A Command-Line Interface (CLI) FTP server and client built in Python using socket programming.

> “d” stands for Darwin, the creator of this project. 🙂

## Features
- Transfer files between client and server.

- Execute OS commands on the client or server (where allowed).

- Fully CLI-based, lightweight, and simple to use.

- Handles large files efficiently with chunked transfers.

- simultanious connections are accepted on server

## Setup
- In `client.py`, update the `HOST` variable to your server's IP address before running.

## Known Issues
- If the client close the program unexpectedly, the server may show a connection error. 
  (Will be fixed in future updates.)


## USAGE:
- first  `pip install -r requirement.txt`

- `commands = [ls,pwd,cd,send filepath/filename ,get filepath/filename]`

  
- server has no control means , you can not do anything using server except for closing it using `q` then press `enter`
   
- client commands starts with `!` ,example if you want to see client's current dir then write `!ls`
  
- server side navigation and commands : you can use commands normally

- Starts server first then connect the client

- Termination of the connection will be from client side : just press `ctrl+c`


## License

- MIT License — free to use with credit to the creator.
