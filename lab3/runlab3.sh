#! /usr/bin/bash

printf "Weather:"
printf "\n"
printf "google:"
printf "\n"
curl http://127.0.0.1:5000/weather/google.com
printf "\n"
printf "yahoo(Domain Name):"
printf "\n"
curl http://127.0.0.1:5000/weather/yahoo.com
printf "\n"
printf "amazon:"
printf "\n"
curl http://127.0.0.1:5000/weather/52.94.236.248      #amazon
printf "\n"
printf "yahoo(IP):"
printf "\n"
curl http://127.0.0.1:5000/weather/98.137.11.164      #yahoo
printf "\n"
printf "\n"
printf "addresses:"
printf "\n"
printf "yahoo(IP):"
printf "\n"
curl http://127.0.0.1:5000/address/98.137.11.164     #yahoo
printf "\n"
printf "amazon:"
printf "\n"
curl http://127.0.0.1:5000/address/52.94.236.248     #amazon
printf "\n"
printf "youtube:"
printf "\n"
curl http://127.0.0.1:5000/address/youtube.com
printf "\n"
printf "yahoo(Domain Name):"
printf "\n"
curl http://127.0.0.1:5000/address/yahoo.com
printf "\n"
