FROM waggle/plugin-tensorflow:2.0.0-armv7l
COPY . .
WORKDIR /src
RUN pip3 install --upgrade pip
RUN pip3 install -r /src/requirements.txt
ARG SAGE_USER_TOKEN="-10"
ARG SAGE_HOST="HOST"
ARG BUCKET_ID_MODEL="BUCKET_ID_MODEL"
RUN mkdir -p /data/model/
RUN sage-cli.py storage files download ${BUCKET_ID_MODEL}  model.tflite --target /data/model/model.tflite
#ADD /data/model/model.tflite /data/model/model.tflite
ENV WAGGLE_PLUGIN_ID="50" \
    WAGGLE_PLUGIN_NAME="Smoke Detection Model" \
    WAGGLE_PLUGIN_REF="https://github.com/iperezx/edge-plugins/tree/master/plugin-smokedetect" \
    SAGE_USER_TOKEN=${SAGE_USER_TOKEN} \
    SAGE_HOST=${SAGE_HOST} \
    BUCKET_ID_MODEL=${BUCKET_ID_MODEL}
CMD [ "python3","/src/main.py" ]
