#! /usr/bin/env python3

import sys
from socket import *
from urllib.parse import urlparse


def main():
    finalDes = sys.argv[1]
    portNum = sys.argv[2]
    url = sys.argv[3]
    urlparse("scheme://netloc/path;parameters?query#fragment")
    o = urlparse(url)
    httPath = str(o.path)
    httpRequest = "GET "+httPath+" HTTP/1.1\r\nHost: "+o.hostname+"\r\n\r\n"
    
    servername = o.hostname
    serverport = int(portNum)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((servername, serverport))
    clientSocket.send(httpRequest.encode())
    modifiedInp = clientSocket.recv(1000) 
    modifiedInp = modifiedInp.decode()
    li = list(modifiedInp.split("\n"))
    for i in li:
        if i.startswith("Content-Length"):
            size = i[15:].strip()
            size = int(size)
    modifiedInp = clientSocket.recv(size)
    modifiedInp = modifiedInp.decode()
    #print(modifiedInp)
    if finalDes == 'f':
        file = open("lab4output",'w')
        file.write('from server: '+modifiedInp)
        file.close()
    if finalDes == 's':
        print('from server: ', modifiedInp)
    clientSocket.close()
    

if __name__ == "__main__":
    main()

