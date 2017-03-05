#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :
'''
@author Adrià Bonet Vidal
Daily free book of Packt notifier
'''

import sys
import json
import requests

apikey = None

class Client(object):

    location = "Lleida"
    url_base = "http://api.wunderground.com/api/"

    url_service = { 
    "hourly" : "/hourly/q/CA/",
    "almanac" : "/almanac/q/CA/",
    "conditions" : "/conditions/q/CA/"
    }


    def __init__(self, apikey):
        super(Client, self).__init__();
        self.apikey = apikey

    # Gets the weather in general (cloudy, rain) and the average humidity
    def hourly_weather(self, json_data):

        humidity = 0
        lenght = len(json_data["hourly_forecast"])
        weather = {}

        for hour in json_data["hourly_forecast"]:
            humidity = humidity + int(hour["humidity"])
            weather.setdefault(hour["condition"], 1)
            weather[hour["condition"]] = weather[hour["condition"]] +1
            
        best = 0
        for item in weather:
            con = weather[item]
            if con > best:
                best = con
                avWeather = item

        humidityAv = humidity/lenght

        return avWeather, humidityAv  

    # Gets the lowest and highest temperature of the day
    def almanac(self, json_data):

        hTemp = json_data["almanac"]["temp_high"]["normal"]["C"]
        lTemp = json_data["almanac"]["temp_low"]["normal"]["C"]

        return hTemp, lTemp

    # Gets the actual temperature and the atmospherical pressure
    def condition(self, json_data):
        
        actualT = json_data["current_observation"]["temp_c"]
        pressure = json_data["current_observation"]["pressure_mb"]

        return actualT, pressure

    def main(self):

        urlHourly = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["hourly"]) + str(self.location) + ".json"

        urlAlmanac = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["almanac"]) + str(self.location) + ".json"

        urlCond = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["conditions"]) + str(self.location) + ".json"

        # Gets the webs in json format
        r = requests.get(urlHourly)
        jsonHourly = json.loads(r.text)

        r = requests.get(urlAlmanac)
        jsonAlmanac = json.loads(r.text)
 
        r = requests.get(urlCond)
        jsonCond = json.loads(r.text)

        # Gets the relevant information of the data 
        cond, humidity = self.hourly_weather(jsonHourly)
        hTemp, lTemp = self.almanac(jsonAlmanac)
        actualT, pressure = self.condition(jsonCond)

        print "\nThe actual weather is "+ cond
        print "The actual temperature is " + str(actualT) +"ºC"
        print "The highest and lowest temperatures will be " \
            +str(hTemp)+"ºC and "+str(lTemp)+"ºC"
        print "The humidity will be "+ str(humidity)+"%"

        print ""
        if int(actualT) <= 20:
            print "You should get a jacket if you are going to go out"
        elif int(actualT) > 20 and int(actualT) <= 30:
            print "There won't be extreme temperatures, so you" +\
                "can go out without a jacket" 
        elif int(actualT) > 30:
            print "There's a hell out of here, take this in mind if" +\
                "you are going to go out"

        if cond == "Clear" or "Cloudy" in cond.split(" "):
            if int(pressure) < 1020:
                print "The weather in general it's OK but can rain "+ \
                    "because of the low pressure, be careful"
            if int(pressure) > 1020:
                print "The weather it's OK and probably won't rain, "+ \
                    "don't worry"
        elif "Rain" in cond.split(" "):
            print "If it's not raining probably it will rain later, "+ \
                "so grab an umbrella"
        else: 
            print "Today will be an average day on your life"+ \
                "don't worry about weather"

        print "\n"

if __name__ == "__main__":

    if not apikey:
        try:
            apikey = sys.argv[1]
        except IndexError:
            print "You have to give an argument with an API key"

    weatherClient = Client(apikey)
    weatherClient.main()