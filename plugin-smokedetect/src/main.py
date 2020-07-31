import numpy as np
import inference,hpwren,composableSys
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
import waggle.plugin,logging,requests
from distutils.util import strtobool

object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)
HPWRENFLAG = strtobool(os.getenv('HPWREN_FLAG'))
#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/\
stations?camera=only&selection=\
boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
cameraID=0
siteID=0
camObj = hpwren.cameras(hpwrenUrl)

if HPWRENFLAG:
    serverName = 'HPWREN Camera'
    imageURL,description = camObj.getImageURL(cameraID,siteID)
else:
    #Playback server
    serverName = 'Playback Server'
    imageURL = 'http://playback:8090/bottom/image.jpg'
    description = 'Playback server image'

#triger setup
urlWindEvents = 'https://wind.events/auth'
proxyUrl = 'https://wifire-api-proxy.nautilus.optiputer.net'
trigger = composableSys.trigger(urlWindEvents,proxyUrl)
counter = 0

#For plugin
plugin = waggle.plugin.Plugin()
print('Starting smoke detection inferencing')
while True:
    testObj = inference.FireImage()
    print('Get image from ' + serverName)
    print("Image url: " + imageURL)
    print("Description: " + description)
    testObj.urlToImage(imageURL)
    interpreter = tflite.Interpreter(model_path=modelPath)
    interpreter.allocate_tensors()
    print('Perform an inference based on trainned model')
    result,percent = testObj.inference(interpreter)
    print(result)
    currentDT = str(datetime.datetime.now())
    
    plugin.add_measurement({
        'id': 1,
        'sub_id':10,
        'value': percent,
    })

    print('Publish\n', flush=True)
    plugin.publish_measurements()

    if (counter == 0 or (result == "Fire" and percent > 0.75)):
        ensembleLatLongList = getEnsembleLatLongList([32.848132, -116.805901])
        params = trigger.getDefaultParams()
        for latLong in ensembleLatLongList:
            params['ignition']['point'] =  latLong
            params['webhook']['request_id'] = str(counter)
            counter += 1
            returnStatus = trigger.launchFarsiteModel(params)

    time.sleep(5)

def getEnsembleLatLongList(latLong):
    returnList = []
    x = 0.01
    for i in range(1,5):
        returnList.append([latLong[0] + x, latLong[1] + x])
    return returnList