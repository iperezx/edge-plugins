# edge-plugins/plugin-smokedetect

## Docker container usage
-------------
The docker image is hosted on [sagecontinuum](https://hub.docker.com/orgs/sagecontinuum).
Before building the image make sure that the environment variables (`SAGE_HOST`, `SAGE_USER_TOKEN`, and `BUCKET_ID_MODEL`) are set in the user's local enviroment.

Set enviroment variables:
```
export SAGE_HOST=https://sage-storage-api.nautilus.optiputer.net
export SAGE_USER_TOKEN=SAGE_USER_TOKEN
export BUCKET_ID_MODEL=BUCKET_ID_MODEL
```
To obtain a token, visit the [Sage Authorization UI](https://sage.nautilus.optiputer.net).
The `BUCKET_ID_MODEL` has been set public so any SAGE user can access the smoke detection models.

Build the image:
```
docker build --build-arg SAGE_HOST=${SAGE_HOST} --build-arg SAGE_USER_TOKEN=${SAGE_USER_TOKEN} --build-arg BUCKET_ID_MODEL=${BUCKET_ID_MODEL} -t sagecontinuum/plugin-smokedetect:0.2.0 .
```
where the `--build-arg` adds all the necessary enviroment variables for the [Sage Storage API](https://github.com/sagecontinuum/sage-storage-api) and [Sage CLI](https://github.com/sagecontinuum/sage-cli)

Run the container:
```
docker run sagecontinuum/plugin-smokedetect:0.2.0
```
# Instructions
The following instructions are meant to serve a user from start to finish of how to create the smoke detection plugin.

## Step 1: clone beehive repository 
```
git clone https://github.com/waggle-sensor/beehive-server
```
Start the server:
```
cd beehive-server
./do.sh deploy
```

## Step 2: run trainning jupyter notebook and save model
First clone the smoke detection model:
```
git clone https://gitlab.nautilus.optiputer.net/i3perez/keras-smoke-detection
```
### Training on a Kubernetes Cluster (on Nautilus):
Create a persistent volume claim on Nautilus under Sage namespace:
```
kubectl create -f keras.pvc.yaml
```

Create a deployment on kubernetes:
```
kubectl create -f kerasDeloyment.yaml
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
If there is no kubernetes cluster available for the user, there is a docker file that can be used to run on the local node (assuming that there is a GPU available).

Build docker image:
```
docker build  -t sagecontinuum/smokeDetecTrainModel .
```

Run docker image:
```
docker run -it -p 9000:9000 sagecontinuum/smokeDetecTrainModel
```
Attach to container and run jupyter notebook:
```
docker attach sagecontinuum/smokeDetecTrainModel
jupyter notebook --ip 0.0.0.0 --port 9000 --no-browser --allow-root
```
Access the notebook through your desktops browser on http://localhost:9000 

### Final Step
Run the juputer notebook as describe in the [README file](https://gitlab.nautilus.optiputer.net/i3perez/keras-smoke-detection/-/blob/master/README.md). At the end of the notebook
the trainned model will be save to the object storage through [SAGE Storage API](https://github.com/sagecontinuum/sage-storage-api)

## Step 3: clone waggle repository
```
git clone https://github.com/waggle-sensor/waggle-node
```
To start the waggle node (this assumes an existing beehive instance):
```bash
./waggle-node up
```

To start a plugin you will need to create a docker image(see Docker container usage section) and pass the following command:
```bash
./waggle-node schedule sagecontinuum/plugin-smokedetect:0.2.0
```
To view the output:
```bash
./waggle-node logs | grep plugin
```

Example output of the plugin:
```
plugin-50-0.1.0-0_1     | published measurements:
plugin-50-0.1.0-0_1     | {'sensor_id': 1, 'sensor_instance': 0, 'parameter_id': 10, 'timestamp': 1584738130, 'value': 0.5205857753753662}
plugin-50-0.1.0-0_1     | Get image from HPWREN Camera
plugin-50-0.1.0-0_1     | Image url: https://hpwren.ucsd.edu/cameras/L/bm-n-mobo-m.jpg
plugin-50-0.1.0-0_1     | Description: Big Black Mountain ~north view, monochrome
plugin-50-0.1.0-0_1     | Perform an inference based on trainned model
plugin-50-0.1.0-0_1     | FIRE, 52.06%
plugin-50-0.1.0-0_1     | Publish
```
