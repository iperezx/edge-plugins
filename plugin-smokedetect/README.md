# edge-plugins/plugin-smokedetect

## Docker container usage
-------------
The docker image is hosted on [sagecontinuum](https://hub.docker.com/orgs/sagecontinuum).
Before building the image make sure that the environment variables (`SAGE_HOST`, `SAGE_USER_TOKEN`,`BUCKET_ID_MODEL`, `APIKEY`,`WINDEVENTSTOKEN`,and `WINDEVENTSPASSWORD`) are set in the user's local enviroment.

Set enviroment variables:
```
export SAGE_STORE_URL=https://sage-storage-api.nautilus.optiputer.net
export SAGE_USER_TOKEN=SAGE_USER_TOKEN
export BUCKET_ID_MODEL=BUCKET_ID_MODEL
export AUTHUSERNAME=AUTHUSERNAME
export AUTHPASSWORD=AUTHPASSWORD
```
To obtain a token, visit the [Sage Authorization UI](https://sage.nautilus.optiputer.net).
The `BUCKET_ID_MODEL` has been set public so any SAGE user can access the smoke detection models.

Build the image:
```
docker build --build-arg SAGE_STORE_URL=${SAGE_STORE_URL} --build-arg SAGE_USER_TOKEN=${SAGE_USER_TOKEN} \
--build-arg BUCKET_ID_MODEL=${BUCKET_ID_MODEL} --build-arg AUTHUSERNAME=${AUTHUSERNAME} --build-arg AUTHPASSWORD=${AUTHPASSWORD} -t sagecontinuum/smoke-detection-plugin:composableSys .
```
where the `--build-arg` adds all the necessary enviroment variables for the [Sage Storage API](https://github.com/sagecontinuum/sage-storage-api) and [Sage CLI](https://github.com/sagecontinuum/sage-cli)

Run the container(optional since the waggle-node will run it automatically):
```
docker run sagecontinuum/smoke-detection-plugin:composableSys
```

Example output of the plugin:
```bash
Get image from HPWREN Camera
Image url: https://hpwren.ucsd.edu/cameras/L/bm-n-mobo-m.jpg
Description: Big Black Mountain ~north view, monochrome
Perform an inference based on trainned model
No Fire, 58.28%
Publish
```


## Optional: run trainning jupyter notebook and save model
There are two options to train the smoke detection neural network. The first one is to
run the jupyter notebook on a Kubernetes cluster (for us it is temporarily going to be [Nautilus](https://nautilus.optiputer.net/)). The second option is to run it locally assuming that there is a GPU availabe on the local node (the docker image might fail but Tensorflow will not).
### Training on a Kubernetes Cluster (Nautilus):
Clone the smoke detection model:
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
docker build --build-arg SAGE_HOST=${SAGE_HOST} --build-arg SAGE_USER_TOKEN=${SAGE_USER_TOKEN} --build-arg BUCKET_ID_MODEL=${BUCKET_ID_MODEL} -t iperezx/training-smokedetect:0.1.0 .
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