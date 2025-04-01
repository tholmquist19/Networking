#! /usr/bin/env python3

import sys
from socket import *
from urllib.parse import urlparse
from scapy.all import *
import json
import socket
import subprocess, shlex



def main():
    url = sys.argv[1]
    urlparse("scheme://netloc/path;parameters?query#fragment")
    o = urlparse(url)
    httPath = str(o.path)
    httpRequest = "GET "+httPath+" HTTP/1.1\r\nHost: "+o.hostname+"\r\nConnection: close\r\n\r\n"
    ip = socket.gethostbyname(o.hostname)
    ip_p = IP()
    ip_p.dst = ip
    t_p = TCP()
    t_p.seq = 5
    t_p.dport = 80
    t_p.sport = 1234
    t_p.flags="S"
    send_p = ip_p/t_p
    p = sr1(send_p)
    t_p.seq = p.ack
    t_p.flags = "A"
    t_p.ack = p.seq+1
    send_p2 = ip_p/t_p
    send(send_p2)
    t_p.flags = "AP"
    send_p3 = ip_p/t_p
    sr1(send_p3/httpRequest)
    



if __name__ == "__main__":
    main()
