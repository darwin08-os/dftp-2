# dftp-2
ftp server client made in python using socket prograaming after some time and testing i will write how you can use this properly like what commands are valid or not and all and this is totally CLI based ftp, "d" there because it is made by darwin means ME.. : )

## Setup
- In `client.py`, update the `HOST` variable to your server's IP address before running.

## Known Issues
- If the client closes unexpectedly, the server may show a connection error. 
  (Will be fixed in future updates.)


## USAGE:
- first  "pip install -r requirement.txt"

- commands = [ls,pwd,cd,send filepath+name ,get filepath+name]

  
- server has no control means from server you cant run any commands
   
- client commands starts with "!" ,example if you want to see client's current dir then write "!ls"
  
- server side navigation and commands : you can use commands normally

