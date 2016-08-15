#!/usr/bin/python
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess
import includes.data as data

def getLocalData():
    """get the locale info from Google Maps and save as JSON formatted object to file"""    
    
    try: 
        currentLocationInfo = data.getCurrentLatLong()
        localeURL = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(currentLocationInfo['latitude']) + ',' + str(currentLocationInfo['longitude'])
        localeInfo = json.loads(subprocess.check_output(['curl', localeURL]))

        # create serializeable class for use to save locale info to JSON file object
        localeDetails = LocaleDetails()
        localeDetails.address = str(localeInfo['results'][0]['formatted_address'])
        localeDetails.area = str(localeInfo['results'][1]['formatted_address'])
        localeDetails.city = str(localeInfo['results'][2]['formatted_address'])
        localeDetails.zipcode = str(localeInfo['results'][3]['formatted_address'])
        localeDetails.county = str(localeInfo['results'][4]['formatted_address'])
        localeDetails.country = str(localeInfo['results'][5]['formatted_address'])

        # create or rewrite data to locale data file as JSON
        data.saveJSONObjToFile('locale.data', localeDetails)
        
    except (Exception):
        
        # try again in 5 seconds if GPS data not ready yet
        time.sleep(5)
        getLocalData()
    
class LocaleDetails:
    '''Locale Information as class to persist as JSON information to file'''
    address = ''
    area = ''
    city = ''
    zipcode = ''
    county = ''
    country = ''
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

# get local locale info every 5 minutes to file to be further processed
getLocalData()
while True:
    getLocalData()
    time.sleep(300)
