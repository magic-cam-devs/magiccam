#!/bin/bash

MODEL_NAME='stargan'
MODEL_VERSION='0.0.2'

# Start Tensorflow Serving container and listening at port 8501
docker run -it --rm -p 8501:8501 \
  kimninh1610/${MODEL_NAME}_serving:$MODEL_VERSION