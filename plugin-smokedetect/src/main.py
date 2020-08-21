import numpy as np
import inference,hpwren,composableSys
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess,random
#import waggle.plugin,logging,requests
from distutils.util import strtobool


object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)
#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/\
stations?camera=only&selection=\
boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
camObj = hpwren.cameras(hpwrenUrl)
numWorkingSites = 40
siteID = random.randrange(numWorkingSites)
numCamerasAtSite = camObj.getNumOfCamerasAtSite(siteID)
serverName = 'HPWREN Camera'

#triger setup
urlWindEvents = 'https://wind.events/auth'
proxyUrl = 'https://wifire-api-proxy.nautilus.optiputer.net'
trigger = composableSys.trigger(urlWindEvents,proxyUrl)
counter = 0

#For plugin
# plugin = waggle.plugin.Plugin()
print('Starting smoke detection inferencing')
while True:
    print('Get image from ' + serverName)
    print('Site ID: ' + str(siteID))
    print('Site Name: ' + camObj.getSiteName(siteID))
    print('Number of Cameras on site for inference: ' + str(numCamerasAtSite))
    for cameraID in range(numCamerasAtSite):
        testObj = inference.FireImage()
        imageURL,description = camObj.getImageURL(cameraID,siteID)
        print("Image url: " + imageURL)
        print("Description: " + description)
        testObj.urlToImage(imageURL)
        interpreter = tflite.Interpreter(model_path=modelPath)
        interpreter.allocate_tensors()
        print('Perform an inference based on trainned model')
        result,percent = testObj.inference(interpreter)
        print(result)
        currentDT = str(datetime.datetime.now())

        if (counter == 0 or ("Fire" in result and percent > 0.75)):
            print('Trigger: Launch Ensemble')
            ensembleLatLongList = trigger.getEnsembleLatLongList([32.848132, -116.805901])
            params = trigger.getDefaultParams()
            for latLong in ensembleLatLongList:
                params['ignition']['point'] =  latLong
                params['webhook']['request_id'] = str(counter)
                counter += 1
                returnStatus = trigger.launchFarsiteModel(params)

        print(' ')
        time.sleep(5)
    print(' ')