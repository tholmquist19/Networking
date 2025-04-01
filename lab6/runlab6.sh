#! /usr/bin/bash
sudo iptables -I OUTPUT -p tcp --tcp-flags ALL RST -j DROP

sudo ./lab6.py "http://httpforever.com/"
sudo ./lab6.py "https://www.yahoo.com/"
sudo ./lab6.py "https://www.dominos.com/en/"


sudo iptables -D OUTPUT -p tcp --tcp-flags ALL RST -j DROP
