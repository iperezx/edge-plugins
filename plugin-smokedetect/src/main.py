import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
import waggle.plugin,logging,requests

object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)

#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/\
stations?camera=only&selection=\
boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
cameraID=0
siteID=0
camObj = hpwren.cameras(hpwrenUrl)
imageURL,description = camObj.getImageURL(cameraID,siteID)

#For plugin
plugin = waggle.plugin.Plugin()

print('Starting smoke detection inferencing')
while True:
    testObj = inference.FireImage()
    print('Get image from HPWREN Camera')
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
        'sensor_id': 1,
        'parameter_id':10,
        'value': percent,
    })

    print('Publish\n', flush=True)
    plugin.publish_measurements()
    time.sleep(5)

