import base64
import json
import os
import requests
import numpy as np
import io
import PIL.Image

from typing import List


class ImageTransformer:

    def __init__(self):
        self._tf_serving_host = ''
        self._tf_serving_port = 8501
        self._model_name = ''
        self._model_version = '001'
        self._image_width = 0
        self._image_height = 0

    def get_label(self,
                  selected_attrs: List[str]) -> List[int]:
        return [0, 0, 0, 0, 0]

    def resize_image_if_need(self, image_bytes: bytes) -> bytes:
        bytesio = io.BytesIO(image_bytes)
        image = PIL.Image.open(bytesio)
        (w, h) = image.size

        if w == self._image_width and h == self._image_height:
            image.close()
            return image_bytes

        image = image.resize((self._image_width, self._image_height))
        bytesio = io.BytesIO()

        saved_format = 'jpeg'
        if image.mode in ('RGBA', 'P'):
            saved_format = 'png'

        image.save(bytesio, format=saved_format)
        image.close()
        return bytesio.getvalue()

    def transform(self,
                  image_bytes: bytes,
                  selected_attrs: List[str]) -> bytes:
        image_bytes = self.resize_image_if_need(image_bytes)
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
        "black_hair": 1,
        "blond_hair": 1,
        "brown_hair": 1,
        "male": 1,
        "female": 0,
        "young": 1,
        "old": 0
    }

    attr2idx = {
        "black_hair": 0,
        "blond_hair": 1,
        "brown_hair": 2,
        "male": 3,
        "female": 3,
        "young": 4,
        "old": 4
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
        self._image_width = 128
        self._image_height = 128

    def get_label(self,
                  selected_attrs: List[str]) -> List[int]:

        attr2bin = HaircolorGenderAgeTransformer.attr2bin
        attr2idx = HaircolorGenderAgeTransformer.attr2idx

        label = [1, 0, 0, 0, 1]

        for attr in selected_attrs:
            if attr.endswith("hair"):
                label[:3] = [0, 0, 0]

            if attr not in attr2bin or attr not in attr2idx:
                raise ValueError('attrs: {} not valid'.format(attr))

            label[attr2idx[attr]] = attr2bin[attr]

        return label
