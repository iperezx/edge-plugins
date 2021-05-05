ARG cuda_version=10.0
ARG cudnn_version=7
FROM nvidia/cuda:${cuda_version}-cudnn${cudnn_version}-devel

RUN apt-get update \
  && apt-get install -y \
  python3-dev \
  python3-pip \
  libatlas-base-dev \
  libhdf5-dev \
  libsm6 \
  libxext6 \
  libxrender-dev \
  git \
  wget \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /userdata/kerasData
