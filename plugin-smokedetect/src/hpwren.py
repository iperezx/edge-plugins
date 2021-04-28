import os
import requests
from requests.exceptions import HTTPError

class cameras:
    def __init__(self,hpwrenUrl):
        self.hpwrenUrl = hpwrenUrl
        self.setHPWRENCamsData()

    def setHPWRENCamsData(self):
        try:
            self.requestData = requests.get(self.hpwrenUrl)
            self.requestData.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')

        self.hpwrenCams = self.requestData.json()


    def getImageURL(self, cameraID=0,siteID=0):
        hpwrenCams = self.hpwrenCams
        hpwrenCamsF = hpwrenCams["features"]
        hpwrenCamsAtSite = hpwrenCamsF[siteID]["properties"]["latest-images"]
        imageURL = hpwrenCamsAtSite[cameraID][0]["image"]
        description = hpwrenCamsAtSite[cameraID][0]["description"]
        return imageURL,description
