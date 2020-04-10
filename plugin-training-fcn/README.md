### Training Resnet101-FCN network on PyTorch
The plugin trains fcn models: resnet101 based fcn101 and fcn50, vgg16 based fcn32, fcn16, and fcn8 (total 5 models). To run the plugin, the user must have Docker engine (greater than 18.X.X) installed on the host. Nvidia CUDA driver (>= 10.1) on the host is preferrable for GPU acceleration.

1) Preparing Dataset

Image dataset needs to be prepared on the host machine and the root path of the dataset will be mounted onto the plugin container. For training labeled images are also required. The following files and folders need to be prepared as well.

- `image` is a folder containing all images
- `gt_image` is a folder containing all labeled (ground truth) images
- `class_names.list` is a file containing class names; one class name per line
- `color_names.list` is a file containing RGB color value for each class; one class color set per line (R, G, B)

2) Preparing Model Configuration

- `config.list` (or other file name that user named) is a file containing configuration of the training as shown below; user can add additional configuration for their use (The possible pair of backbone and fcn are: `{resnet, 101}, {resnet, 50}, {vgg, 32s}, {vgg, 16s}, {vgg, 8s}`:
```
{
    "max_iteration": 100000, 
    "lr": 1e-10, 
    "momentum": 0.99, 
    "weight_decay": 0.0005, 
    "interval_validate": 4000,
    "backbone": "resnet",
    "fcn": "101",
    "log_dir": "resnet101"
}
```

3) Pre-trained models

The plugin requires a pre-trained fcn model with regard to what the user is tyring to train. The user need to provide the pre-trained models with regard to request.

- `pretrained_models` is a folder containing pre-trained PyTorch models such as fcn32s_from_caffe.pth


**All of the files and folders (total 2 files and 3 folders) must be in one folder, and the folder needs to be mounted as `/storage`**


4) Training

To train, simply run the command below on the host machine. Please make sure to set all the path correct.


```
# skip --runtime nvidia if the host is not CUDA accelerated
docker run -d --rm \
  --runtime nvidia \
  --shm-size 16G \
  -v ${PATH_FOR_INPUT_IMAGES_FOLDER}:/storage \
  ${DOCKER_IMAGE_NAME} \
  --config ${FILE_NAME: default=config.list} 
```

The log of the training can be shown by,

```
docker logs -f ${DOCKER_IMAGE_NAME}
```

After the training is completed checkpoint models and logs can be found in `/storage/${MODEL_NAME}` on the host machine. The logs can be rendered by `tensorboard`.

```
$ tensorboard --logdir ${PATH_TO_LOGS}
```


### Adjustment required:

- VGG based training method need to be checked (the models are not learnt throught the method).

