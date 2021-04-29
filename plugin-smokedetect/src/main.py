import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
import waggle.plugin,logging,requests
from distutils.util import strtobool
import argparse

numWorkingSites = 30
totalCameraTypes = 1

mainDescription = 'Run smoke detection plugin for a specified HPWREN camera.'
parser = argparse.ArgumentParser(description=mainDescription)
# Add cameraType and siteID
parser.add_argument('--siteID', metavar='siteID', type=int, choices=range(0,numWorkingSites), help='HPWREN camera site ID')
parser.add_argument('--cameraType', metavar='cameraType',choices=range(0,totalCameraTypes), type=int, help='HPWREN camera ID')
args = parser.parse_args()
cameraType=args.cameraType
siteID=args.siteID

object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)

#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/"\
"stations?camera=only&selection="\
"boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
camObj = hpwren.cameras(hpwrenUrl)
serverName = 'HPWREN Camera'
imageURL,description = camObj.getImageURL(cameraType,siteID)

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
    time.sleep(5)

