#! /usr/bin/env python3
import sys
import requests
import json
import socket
import requests
import subprocess, shlex


def main():
    # base API string for weather.gov
    weather_s = "https://api.weather.gov/points/"

    
    # sys.argv[1] gives us the command line input
    # sys.argv[0] is the name of the python file
    print(weather_s+sys.argv[1])

    '''
    # use the commandline input and the weather_s to make API call
    response = requests.get(weather_s+sys.argv[1])

    # convert it to json
    js = json.loads(response.text)

    # find the forecast URL based on the API page
    forecast_URL = js['properties']['forecast']

    #print link that we use for next API call
    print(forecast_URL)

    # call the API again to get theforecast
    final_response = requests.get(forecast_URL)

    #parse json
    js = json.loads(final_response.text)

    #print the forecast
    print(js['properties']['periods'][0]['detailedForecast'])
    
    '''
    #pull the ip address from the url provided
    ip = socket.gethostbyname(sys.argv[1])
    
    #run the whois command for the ip address then save it to a string and then parse the string into a list splitting on each \\n character
    loc = str(subprocess.check_output(["whois",ip]))
    li = list(loc.split("\\n"))
    
    #iterate through the list made by the whois output and find the address, city, state, and zip code of the ip address for the url provided then assign them to variables that can be used later
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
        
    
    #take the address string and separate each peace of it to be used for the url in the api call
    addrList = list(address.split(" "))
    
    #format the address string to fit the specifications of the api call
    addrInput = ""
    count =0
    for i in addrList:
        addrInput+=i+"+"
        count+=1
    addrInput = addrInput[:-1]
    addrInput+="%2C"+city+"%2C"+state+"%2C"+postal
    
    #call the api to give us the coordinates of the region we have specified using the string we just created
    latLon = requests.get("https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address="+addrInput+"%2C+20233&benchmark=2020&vintage=2010&format=json")
    
    #parse the json output into text so that we can use it, then use that to find the x and y coordinates of our specified region
    par = json.loads(latLon.text)
    x = par['result']['addressMatches'][0]['coordinates']['x']
    y = par['result']['addressMatches'][0]['coordinates']['y']
    
    
    #create a string with the x an y coordinates that will fit the specifications of the weather api then feed that string into the api to get the detailed forecast for that location
    coord = str(y)+","+str(x)
    res = requests.get(weather_s+coord)
    
    #take the output from the api and convert it to text so we can work with it
    jso = json.loads(res.text)
    
    #parse through the output to find the detailed forecast then display the forecast provided by the api
    fore_URL = jso['properties']['forecast']
    final_res = requests.get(fore_URL)
    jso = json.loads(final_res.text)
    fore = jso['properties']['periods'][0]['detailedForecast']
    print(fore)
    

if __name__ == "__main__":
    main()

