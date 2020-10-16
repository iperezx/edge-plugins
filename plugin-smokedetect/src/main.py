import numpy as np
import inference,hpwren
import tflite_runtime.interpreter as tflite
import time,datetime,os,sys,subprocess
from distutils.util import strtobool
import waggle.plugin as plugin
from waggle.data import open_data_source

object = 'model.tflite'
directory = '/data/model/'
modelPath = os.path.join(directory,object)

#For plugin
serverName = 'data-stream'
plugin.init()

print('Starting smoke detection inferencing')
while(True):
    with open_data_source(id="bottom_image") as cap:
        testObj = inference.FireImage()
        timestamp, image = cap.get()
        testObj.setImage(image)
        interpreter = tflite.Interpreter(model_path=modelPath)
        interpreter.allocate_tensors()
        print('Get image from ' + serverName)
        print('Perform an inference based on trainned model')
        result,percent = testObj.inference(interpreter)
        print(result)
        print('Publish\n', flush=True)
        plugin.publish('env.detection.smoke', result)
        time.sleep(5)