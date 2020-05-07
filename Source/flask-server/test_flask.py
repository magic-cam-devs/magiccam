from app import app
from os.path import join

test_images_dir = 'test_images'


def test_simple_post_request():
    input_bytes = open(join(test_images_dir, '0140ootp_hermione.jpg'), 'rb').read()

    response = app.test_client().post(path='/haircolor-gender-age',
                                      query_string='attrs[]=black_hair&attrs[]=female&attrs[]=young',
                                      data=input_bytes)
    assert response.status_code == 200


def test_missing_attrs_query():
    input_bytes = open(join(test_images_dir, '0140ootp_hermione.jpg'), 'rb').read()

    response = app.test_client().post(path='/haircolor-gender-age',
                                      data=input_bytes)
    assert response.status_code == 400


def test_attrs_not_valid():
    input_bytes = open(join(test_images_dir, '0140ootp_hermione.jpg'), 'rb').read()

    response = app.test_client().post(path='/haircolor-gender-age',
                                      query_string='attrs[]=malee',
                                      data=input_bytes)
    assert response.status_code == 400
