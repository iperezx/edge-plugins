FROM waggle/plugin-tensorflow:2.0.0
COPY . .
WORKDIR /src
RUN pip3 install --upgrade pip
RUN pip3 install -r /src/requirements.txt
RUN mkdir -p /data/model/
ARG SAGE_USER_TOKEN="-10"
ARG SAGE_HOST="HOST"
ARG BUCKET_ID_MODEL="BUCKET_ID_MODEL"
ARG LC_ALL="C.UTF-8"
ARG LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    WAGGLE_PLUGIN_ID="50" \
    WAGGLE_PLUGIN_NAME="Smoke Detection Model" \
    WAGGLE_PLUGIN_VERSION="0.3.0" \
    WAGGLE_PLUGIN_INSTANCE="1" \
    WAGGLE_PLUGIN_REF="https://github.com/iperezx/edge-plugins/tree/master/plugin-smokedetect" \
    SAGE_USER_TOKEN=${SAGE_USER_TOKEN} \
    SAGE_HOST=${SAGE_HOST} \
    BUCKET_ID_MODEL=${BUCKET_ID_MODEL} 
RUN sage-cli.py storage files download ${BUCKET_ID_MODEL}  model.tflite --target /data/model/model.tflite
CMD [ "python3","/src/main.py" ]
