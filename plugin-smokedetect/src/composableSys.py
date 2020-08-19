import os
import requests

class trigger:
    def __init__(self,urlWindEvents,proxyUrl):
        authToken = self.getWindEventsToken(urlWindEvents)
        apiKey = os.getenv('APIKEY')
        self.headers = {'content-type': "application/json",
                        'authorization': 'Bearer ' + authToken['token'],
                        'x-api-key': apiKey}
        self.farsiteParams = self.getDefaultParams()
        self.proxyUrl = proxyUrl
        
    def getWindEventsToken(self,urlWindEvents):
        windEventsToken = os.getenv('WINDEVENTSTOKEN')
        if windEventsToken is None:
            raise EnvironmentError("Failed because {} is not set.".format('WINDEVENTSTOKEN'))
        headers = {'Authorization': 'Basic {}'.format(windEventsToken),'content-type':'application/json'}
        windEventsPassword = os.getenv('WINDEVENTSPASSWORD')
        if windEventsPassword is None:
            raise EnvironmentError("Failed because {} is not set.".format('WINDEVENTSPASSWORD'))
        data = {'user':'wifire','password':windEventsPassword}
        r = requests.request('GET',urlWindEvents,headers=headers,json=data)
        authToken = r.json()
        return authToken

    def getDefaultParams(self):
        defaultParams = {"hours": 3,
                        "ember": 80,
                        "ignition": {
                            "point": [32.848132, -116.805901]
                        },
                        "weather": {
                            "repeat_values": {
                                "wind_direction": 180,
                                "wind_speed": 5,
                                "relative_humidity": 5,
                                "temperature": 70
                            }
                        },
                        "fuel_moisture": {
                            "one_hr": 3, 
                            "ten_hr": 4, 
                            "hundred_hr": 6,
                            "live_herb": 5,
                            "live_woody": 60
                        },
                        "webhook": {
                            "url": "https://wifire-webhook.nautilus.optiputer.net/webhook",
                            "request_id": "2"
                        }
        }
        return defaultParams

    def getEnsembleLatLongList(self,latLong):
        returnList = []
        x = 0.01
        for i in range(1,5):
            returnList.append([latLong[0] + x, latLong[1] + x])
        return returnList

    def setParamDict(self,params):
        #Change this to iterate through each dictionary key and assing it to farsiteParams
        self.farsiteParams['ignition']['point'] =  params['ignition']['point']
        self.farsiteParams['webhook']['request_id'] = params['webhook']['request_id']

    def launchFarsiteModel(self,params):
        self.setParamDict(params)
        r = requests.request('POST',self.proxyUrl,headers=self.headers,json=self.farsiteParams)
        return r.text

