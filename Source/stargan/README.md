

# Dependencies

## Install with pip:
Python 3.5.x +

Select your tensorflow version in requirments.txt (CPU or GPU), then run this command

`
pip install -r requirments.txt
`

## Install with conda:
`
`

## Install with Docker
`
`

# Start Tensorflow Serving

First, download the model checkpoint:
```bash
python download.py --type checkpoint
```

Then, download the dataset label:
```bash
python download.py --type labels
```

Export the model to SavedModel format:
```bash
python main.py --phase export
```

Finally, start serving. Make sure that you had installed [Docker](https://docs.docker.com/get-docker/)
```bash
$ ./start_serving_docker.sh
```

Testing the Tensorflow Serving Server:

Start the jupyter notebook first, then open and run [serving_sample_request.ipynb](./notebooks/serving_sample_request.ipynb)