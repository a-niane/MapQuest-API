                            #Lab 4: MapQuest POI
import urllib.parse
import urllib.request
import json

class MapQuest:
    def __init__(self, APIKey = 'D6b0Lh1PIHNgLjurubZOrO0mUjASdDTj'):
        self._API_KEY = APIKey
        self._DIRECTION_URL = 'http://open.mapquestapi.com/directions/v2/route'
        self._GEOCODE_URL = 'http://www.mapquestapi.com/geocoding/v1/address'
        self._PLACES_URL = 'https://www.mapquestapi.com/search/v4/place'

    def totalDistance(self, locations: list)->float:
        if len(locations) < 2:
            return 0.0

        distance = self._DIRECTION_URL 

        url_distance = [] 
        url_distance.append(('key', self._API_KEY)) 

        for i in range(len(locations)): 
            if i == 0:
                url_distance.append(("from", locations[i]))
            else:
                url_distance.append(("to", locations[i]))

        url = distance + '?' + urllib.parse.urlencode(url_distance) 

        stuff = urllib.request.urlopen(url)
        diction = json.load(stuff)
        stuff.close()

        return float(diction['route']['distance'])
        
    def totalTime(self, locations:list)->int:
        if len(locations) < 2:
            return 0

        url_time = []
        url_time.append(('key', self._API_KEY))

        time = self._DIRECTION_URL
        
        for i in range(len(locations)):
            if i == 0:
                url_time.append(("from", locations[i]))
            else:
                url_time.append(("to", locations[i]))

        url = time + '?' + urllib.parse.urlencode(url_time)

        stuff = urllib.request.urlopen(url)
        diction = json.load(stuff) 
        stuff.close()

        return int(diction['route']['time'])
       
    def directions(self, locations:list)->str:
        if len(locations) < 2:
            return ""

        url_direction = []
        url_direction.append(('key', self._API_KEY))

        direction = self._DIRECTION_URL 
        
        for i in range(len(locations)):
            if i == 0:
                url_direction.append(("from", locations[i]))
            else:
                url_direction.append(("to", locations[i]))

        url = direction + '?' + urllib.parse.urlencode(url_direction)

        stuff = urllib.request.urlopen(url)
        diction = json.load(stuff) 
        stuff.close()

        theAnswer = ""

        for directs in diction['route']['legs']:
            for rets in directs['maneuvers']:
                theAnswer += str(rets['narrative']) + '\n'

        return theAnswer
    
    def pointOfInterest(self, locations:str, keyword:str, results:int)->list:
        if locations == "" or keyword == "" or results <= 0:
            return []
        
        geocode = self._GEOCODE_URL

        items = [('key', self._API_KEY), ('location', locations),('q', keyword),('limit', str(results))]

        url_poi = geocode + '?' + urllib.parse.urlencode(items)

        stuff = urllib.request.urlopen(url_poi)
        diction = json.load(stuff)
        stuff.close()

        lat = diction['results'][0]['locations'][0]['latLng']['lat']
        long = diction['results'][0]['locations'][0]['latLng']['lng']
       
        places = self._PLACES_URL

        elems = [('location', str(long) + ", " + str(lat)), ('sort', 'distance'), ('feedback', 'false'), ('key', self._API_KEY), ('limit', results), ('q', keyword)]

        url_true = places + '?' + urllib.parse.urlencode(elems)

        trueopen = urllib.request.urlopen(url_true)
        diction2 = json.load(trueopen)
        trueopen.close()

        count = 0
        finish = []

        for i in range(len(diction2['results'])):
            if count <= results:
                finish.append(diction2['results'][i]['displayString'])
                count += 1
                
        return finish
