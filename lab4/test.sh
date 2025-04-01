#! /usr/bin/bash

printf "\n"
./lab4.py s 80 http://httpforever.com/
./lab4.py f 5000 http://127.0.0.1:5000/weather/google.com
./lab4.py s 5000 http://127.0.0.1:5000/weather/yahoo.com
printf "\n"
./lab4.py s 5000 http://127.0.0.1:5000/address/yahoo.com
printf "\n"


