#!/bin/bash

MODEL_NAME='stargan'
MODEL_VERSION='0.0.2'

docker run -d --name serving_base tensorflow/serving:1.13.1
docker cp ./optimized_saved_model serving_base:/models/$MODEL_NAME
docker commit --change "ENV MODEL_NAME $MODEL_NAME" serving_base \
  kimninh1610/${MODEL_NAME}_serving:$MODEL_VERSION
docker kill serving_base
docker rm serving_base