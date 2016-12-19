#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import os, time, json
import includes.data as data
import includes.postgres as postgres

# save full datasets to DB each second
while True:
    try:
        locationInfo = data.getJSONFromDataFile('location.data')
        localeInfo = data.getJSONFromDataFile('locale.data')
        tempInfo = data.getJSONFromDataFile('temp.data')
        weatherInfo = data.getJSONFromDataFile('weather.data')
        postgres.saveDrivingStats(locationInfo, localeInfo, tempInfo, weatherInfo)    
    except (Exception):
        pass
    time.sleep(1)