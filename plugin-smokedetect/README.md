# edge-plugins/plugin-smokedetect

## Docker container usage
-------------
The docker image is hosted on [sagecontinuum](https://hub.docker.com/orgs/sagecontinuum).

Build the image:
```
docker build  -t sagecontinuum/plugin-smokedetect:ai-gateway-demo .
```
Run the container:
```
docker run sagecontinuum/plugin-smokedetect:ai-gateway-demo --siteID 0 --cameraType 0
```
# Instructions
The following instructions are meant to serve a user from start to finish of how to create the smoke detection plugin.

## Step 1: run trainning jupyter notebook and save model
There are two options to train the smoke detection neural network. The first one is to
run the jupyter notebook on a Kubernetes cluster (for us it is temporarily going to be [Nautilus](https://nautilus.optiputer.net/)). The second option is to run it locally assuming that there is a GPU availabe on the local node (the docker image might fail but Tensorflow will not).
### Training on a Kubernetes Cluster (Nautilus):
```
cd training/
```
Create a persistent volume claim on Nautilus under the Sage namespace (not needed now since it exists):
```
kubectl create -f training.pvc.yaml
```

Create a deployment on kubernetes:
```
kubectl create -f training.deployment.yaml
```

Attach to a pod and run bash:
```
kubectl exec -it POD-NAME bash
```

Run jupyter notebook on pod:
```
jupyter notebook -—ip=0.0.0.0 -—port=9000
```

Port forward from pod to local node:
```
kubectl port-forward POD-NAME 9000:9000
```
Access the notebook through your desktops browser on http://localhost:9000 

### Training on a local node(if no kubernetes cluster is available):
If there is no kubernetes cluster available for the user, there is a docker file that can be used to run on a local node (assuming that there is a GPU available).

Build docker image:
```
docker build -t iperezx/training-smokedetect:0.1.0 .
```

Run docker image:
```
docker run -it -p 9000:9000 iperezx/training-smokedetect:0.1.0
```

Attach to container and run jupyter notebook:
```
docker attach iperezx/training-smokedetect:0.1.0
jupyter notebook --ip 0.0.0.0 --port 9000 --no-browser --allow-root
```

Access the notebook through your desktops browser on http://localhost:9000 

### Final Step
Run the juputer notebook as describe in the [README file](https://gitlab.nautilus.optiputer.net/i3perez/keras-smoke-detection/-/blob/master/README.md). A tensorflow lite model will be automically saved (in the last cell).


## Example output

Example output of the plugin:
```bash
Get image from HPWREN Camera
Image url: http://hpwren.ucsd.edu/cameras/L/bm-n-mobo-c.jpg
Description: Big Black Mountain North Color Original
Perform an inference based on trainned model
Fire, 71.29%
Publish
```

## Setup for MIC to upload model to MINT:

```bash
mic pkg start --name smoke-detection --image sagecontinuum/plugin-smokedetect:ai-gateway-demo
mic pkg trace python3 /src/main.py --cameraType 0 --siteID 0
mic pkg parameters -f mic/mic.yaml -n siteID -v 0 -d 'Input parameter used to provide the hpwren camera site'
mic pkg parameters -f mic/mic.yaml -n cameraType -v 0 -d 'Input parameter used to provide the hpwren camera type'
mic pkg inputs
mic pkg outputs
mic pkg wrapper
mic pkg run
```