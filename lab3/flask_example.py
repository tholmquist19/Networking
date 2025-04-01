from flask import Flask
import subprocess
import socket
import requests
import sys
import json

app = Flask(__name__)

weatherCache = dict()
addrCache = dict()

@app.route("/upper/<echo_string>")
def upper(echo_string):
    return(echo_string.upper())

@app.route("/callwhois")
def whois():
    s,o = subprocess.getstatusoutput("whois 8.8.8.8")
    return(o)

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route("/address/<url>")
def address(url):
    if url in addrCache:
        return(addrCache[url])

    if url.isnumeric():
        ip = int(url)
    else:
        ip = socket.gethostbyname(url)
    loc = str(subprocess.check_output(["whois",ip]))
    li = list(loc.split("\\n"))
    addr = ""
    for i in li:
        if i.startswith("Address:"):
            addr+=i+"\n"
        if i.startswith("City:"):
            addr+=i+"\n"
        if i.startswith("StateProv:"):
            addr+=i+"\n"
        if i.startswith("PostalCode:"):
            addr+=i+"\n"
        if i.startswith("Country:"):
            addr+=i
    li = list(addr.split("\n"))
    address = ""
    city = ""
    state = ""
    postal = ""
    country = ""
    for i in li:
        if i.startswith("Address:"):
            address=i[16:]
            address.strip()
        if i.startswith("City:"):
            city = i[16:]
            city.strip()
        if i.startswith("StateProv:"):
            state=i[16:]
            state.strip()
        if i.startswith("PostalCode:"):
            postal=i[16:]
            postal.strip()
        if i.startswith("Country:"):
            country=i[16:]
            country.strip()    
            
    returnAddr = address+", "+city+", "+state+", "+postal+", "+country
    
    addrCache[url]=returnAddr
    return(returnAddr) 


@app.route("/weather/<url>")
def weather(url):
    weather_s = "https://api.weather.gov/points/"
    if url in weatherCache:
        return(weatherCache[url])
        
    if url.isnumeric():
        ip = int(url)
    else:
        ip = socket.gethostbyname(url)

    loc = str(subprocess.check_output(["whois",ip]))
    li = list(loc.split("\\n"))
    
    addr = ""
    address = ""
    city = ""
    state = ""
    postal = ""
    country = ""
    for i in li:
        if i.startswith("Address:"):
            address=i[16:]
            address.strip()
        if i.startswith("City:"):
            city = i[16:]
            city.strip()
        if i.startswith("StateProv:"):
            state=i[16:]
            state.strip()
        if i.startswith("PostalCode:"):
            postal=i[16:]
            postal.strip()
        
    
    addrList = list(address.split(" "))
    
    addrInput = ""
    count =0
    for i in addrList:
        addrInput+=i+"+"
        count+=1
    addrInput = addrInput[:-1]
    addrInput+="%2C"+city+"%2C"+state+"%2C"+postal
    
    latLon = requests.get("https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address="+addrInput+"%2C+20233&benchmark=2020&vintage=2010&format=json")
    
    par = json.loads(latLon.text)
    x = par['result']['addressMatches'][0]['coordinates']['x']
    y = par['result']['addressMatches'][0]['coordinates']['y']
    
    
    coord = str(y)+","+str(x)
    res = requests.get(weather_s+coord)
    
    jso = json.loads(res.text)
    
    fore_URL = jso['properties']['forecast']
    final_res = requests.get(fore_URL)
    jso = json.loads(final_res.text)
    fore = jso['properties']['periods'][0]['detailedForecast']
    
    weatherCache[url] = fore
    return(fore)

if __name__ == "__main__":
    app.run()
