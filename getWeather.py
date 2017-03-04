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
import warnings


apikey = None
warnings.filterwarnings("ignore")

class Client(object):

    location = "Lleida"
    url_base = "http://api.wunderground.com/api/"

    url_service = { 
    "hourly" : "/hourly/q/CA/",
    "almanac" : "/almanac/q/CA/",
    "astronomy" : "/astronomy/q/CA/",
    "conditions" : "/conditions/q/CA/"
    }




    def __init__(self, apikey):
        super(Client, self).__init__();
        self.apikey = apikey

    def hourly_weather(self, json_data):
        pass

    def almanac(self, json_data):
        pass

    def condition(self, json_data):
        pass

    def main(self):

        urlHourly = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["hourly"]) + str(self.location) + ".json"

        urlAlmanac = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["almanac"]) + str(self.location) + ".json"

        urlCond = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["conditions"]) + str(self.location) + ".json"

        # Hourly: condition -> Chance of Rain , Clear , Partly Cloudy , Mostly Cloudy
        #           humidity -> integer
        r = requests.get(urlHourly)
        jsonHourly = json.loads(r.text)

        # Almanac: temp_high -> normal -> F , C
        #   temp_low ~= temp_high
        r = requests.get(urlAlmanac)
        jsonAlmanac = json.loads(r.text)

        # Conditions: temp_f , temp_c , pressure_mb ->  <1020 = rain   1020-1040 ~ rain 
        r = requests.get(urlCond)
        jsonCond = json.loads(r.text)

        #cond, humidity = self.hourly_weather(jsonHourly)
        #htemp, ltemp = almanac(jsonAlmanac)


if __name__ == "__main__":

    if not apikey:
        try:
            apikey = sys.argv[1]
        except IndexError:
            print "You have to give an argument with an API key"

    weatherClient = Client(apikey)
    weatherClient.main()