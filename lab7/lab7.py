#! /usr/bin/env python3

import sys
from socket import *
from urllib.parse import urlparse
from scapy.all import IP,TCP,sr1,ls
import json
import socket
import subprocess, shlex
import requests



ASCache = dict()

def main():
    url = sys.argv[1]
    urlparse("scheme://netloc/path;parameters?query#fragment")
    o = urlparse(url)
    try:
        ip = socket.gethostbyname(o.hostname)
    except Exception as e:
        ip = str(url) 
    ip_p = IP()
    ip_p.dst = ip
    t_p = TCP()
    t_p.seq = 5
    t_p.dport = 80
    t_p.sport = 1234
    t_p.flags="S"
    send_p = ip_p/t_p
    for x in range(1,31):
        p = sr1(send_p, timeout=3,verbose=0)
        send_p.ttl=x
        if p is not None:
            try:
                domain = socket.gethostbyaddr(p.src)[0]
            except socket.herror:
                domain = "no DNS value found"
            loc = str(subprocess.check_output(["whois","-h","whois.cymru.com",p.src]))
            li = list(loc.split("|"))
            AS = li[2].lstrip(" AS Name"+"\ "+"\ "+"n'").rstrip()
            if AS != "":
                ASCache[AS] = p.src
            print(f"{x}. {p.src},  {domain}")     
        if p is None:
            print(f"{x}. * * *")
        if p is not None and type(p.payload) == TCP and x>1:
            if p.payload.flags == "SA":
                ASlist=list(ASCache.keys())
                print("\nAS's passed through include- "+str(ASlist))
                break



if __name__ == "__main__":
    main()
