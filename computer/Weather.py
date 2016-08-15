#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess
import includes.data as data
import includes.settings as settings

class WeatherDetails:
    '''Weather Information as class to persist as JSON information to file'''
    time = 0
    summary = 0
    icon = 0
    apparentTemperature = 0
    humidity = 0
    precipIntensity = 0
    precipProbability = 0
    windSpeed = 0
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

# remove old file and start logging weather
data.removeJSONFile('weather.data')
while True:

    # get current conditions from API
    currentLocationInfo = data.getCurrentLatLong()
    
    # wait for lat/long info to be available
    if (str(currentLocationInfo['latitude']) ==  '0.0' and str(currentLocationInfo['longitude'] ==  '0.0')):
        time.sleep(1)
        continue
        
    # get current forecast from location
    weatherInfo = json.loads(subprocess.check_output(['curl', 'https://api.forecast.io/forecast/' + settings.weatherAPIKey + '/' + str(currentLocationInfo['latitude']) + ',' + str(currentLocationInfo['longitude']) + '?lang=en']))
    currentConditions = weatherInfo['currently']
    
    # gather info in serializable object to store as JSON file
    weatherDetails = WeatherDetails()
    weatherDetails.time = int(currentConditions['time'])
    weatherDetails.summary = str(currentConditions['summary'])
    weatherDetails.icon = str(currentConditions['icon'])
    weatherDetails.apparentTemperature = float(currentConditions['apparentTemperature'])
    weatherDetails.humidity = float(currentConditions['humidity'])
    weatherDetails.precipIntensity = float(currentConditions['precipIntensity'])
    weatherDetails.precipProbability = float(currentConditions['precipProbability'])
    weatherDetails.windSpeed = float(currentConditions['windSpeed'])

    # create or rewrite data to weather data file as JSON, then wait 5 minutes
    data.saveJSONObjToFile('weather.data', weatherDetails)
    time.sleep(300)
