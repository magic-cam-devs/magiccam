#!/bin/bash

MODEL_PATH="$(pwd)/saved_model"
MODEL_NAME="star_gan"

# Start Tensorflow Serving container and listening at port 8501
docker run -it --rm -p 8501:8501 \
  -v "$MODEL_PATH:/models/$MODEL_NAME" \
  -e MODEL_NAME=$MODEL_NAME \
  tensorflow/serving:1.13.1