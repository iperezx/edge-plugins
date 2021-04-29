import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
from distutils.util import strtobool
import argparse,json

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
workDir = '/src'
modelPath = os.path.abspath(os.path.join(workDir,object))
imageName = 'hpwren-image-used-for-inference.jpeg'
imagePath = os.path.abspath(os.path.join(workDir,imageName))

resultsName = 'model-inference-results.json'
resultsPath = os.path.abspath(os.path.join(workDir,resultsName))

#HPWREN Parameters
hpwrenUrl = "https://firemap.sdsc.edu/pylaski/"\
"stations?camera=only&selection="\
"boundingBox&minLat=0&maxLat=90&minLon=-180&maxLon=0"
camObj = hpwren.cameras(hpwrenUrl)
serverName = 'HPWREN Camera'
imageURL,description = camObj.getImageURL(cameraType,siteID)

#Inference Section
# print('Starting smoke detection inferencing')
testObj = inference.FireImage()
# print('Get image from ' + serverName)
# print("Image url: " + imageURL)
# print("Description: " + description)
testObj.urlToImage(imageURL)
testObj.writeImage(imagePath)

interpreter = tflite.Interpreter(model_path=modelPath)
interpreter.allocate_tensors()
result,percent = testObj.inference(interpreter)
# print('Perform an inference based on trainned model')
# print(result)

#Output section
classifier = result.split(',')[0]
currentDT = str(datetime.datetime.now())
outputDataSchema = ['Image Server','Image URL','Image Description',
                    'Inference Classifier','Inference Accuracy',
                    'Inference Datetime']
outputDataVals = [serverName,imageURL,description,
                    classifier,percent,currentDT]
outputDataDict = {outputDataSchema[i]: outputDataVals[i] for i in range(len(outputDataSchema))}
with open(resultsPath,'w') as fp:
    json.dump(outputDataDict,fp)