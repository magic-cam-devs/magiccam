import base64
import json
import os
import requests
import numpy as np

from typing import List


class ImageTransformer:

    def __init__(self):
        self._tf_serving_host = ''
        self._tf_serving_port = 8501
        self._model_name = ''
        self._model_version = '001'

    def get_label(self,
                  selected_attrs: List[str]) -> List[int]:
        return [0, 0, 0, 0, 0]

    def transform(self,
                  image_bytes: bytes,
                  selected_attrs: List[str]) -> bytes:
        b64_encoded_bytes = base64.b64encode(image_bytes)
        b64_encoded_str = b64_encoded_bytes.decode('utf-8')

        target_domain_label = self.get_label(selected_attrs)
        target_domain_label = np.array(target_domain_label).reshape(1, - 1)

        json_obj = {
            'inputs': {
                'input_bytes': {
                    'b64': b64_encoded_str
                },
                'target_domain_label': target_domain_label.tolist()
            }
        }

        r = requests.post('http://{}:{}/v1/models/{}/versions/{}:predict'
                          .format(self._tf_serving_host,
                                  self._tf_serving_port,
                                  self._model_name,
                                  self._model_version),
                          json=json_obj)

        response = json.loads(r.content.decode('utf-8'))

        if 'error' in response:
            raise SystemError(response['error'])

        output_image_base64_str = response['outputs']['b64']
        output_image_bytes = base64.b64decode(output_image_base64_str)

        return output_image_bytes


class HaircolorGenderAgeTransformer(ImageTransformer):
    attr2bin = {
        "Black_Hair": 1,
        "Blond_Hair": 1,
        "Brown_Hair": 1,
        "Male": 1,
        "Female": 0,
        "Young": 1,
        "Old": 0
    }

    attr2idx = {
        "Black_Hair": 0,
        "Blond_Hair": 1,
        "Brown_Hair": 2,
        "Male": 3,
        "Female": 3,
        "Young": 4,
        "Old": 4
    }

    def __init__(self):
        super().__init__()
        haircolor_gender_age_model_host = os.environ.get('HAIRCOLOR_GENDER_AGE_MODEL_HOST')
        haircolor_gender_age_model_version = os.environ.get('HAIRCOLOR_GENDER_AGE_MODEL_VERSION')

        if haircolor_gender_age_model_host is None:
            raise ValueError('Enviroment variable HAIRCOLOR_GENDER_AGE_MODEL_HOST unset')

        if haircolor_gender_age_model_version is None:
            raise SystemError('Enviroment variable HAIRCOLOR_GENDER_AGE_MODEL_VERSION unset')

        self._tf_serving_host = haircolor_gender_age_model_host
        self._model_name = 'stargan'
        self._model_version = haircolor_gender_age_model_version

    def get_label(self,
                  selected_attrs: List[str]) -> List[int]:

        attr2bin = HaircolorGenderAgeTransformer.attr2bin
        attr2idx = HaircolorGenderAgeTransformer.attr2idx

        label = [1, 0, 0, 0, 1]

        for attr in selected_attrs:
            if attr.endswith("Hair"):
                label[:3] = [0, 0, 0]

            if attr not in attr2bin or attr not in attr2idx:
                raise ValueError('selected_attrs not valid')

            label[attr2idx[attr]] = attr2bin[attr]

        return label
