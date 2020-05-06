import os

from typing import List
from flask import Flask, request, make_response
from transformation import HaircolorGenderAgeTransformer

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))


def str_to_list(string: str, separator: str) -> List[str]:
    return string.split(separator)


@app.route('/haircolor-gender-age', methods=['POST'])
def haircolor_gender_age_transformer():
    image_bytes = request.get_data()
    selected_attrs = request.args.get("selected_attrs")

    if selected_attrs is None:
        return 'Request must include param \'selected_attrs\'', 400

    selected_attrs = str_to_list(selected_attrs, ',')
    print("selected attribute: {}".format(selected_attrs))

    try:
        transformer = HaircolorGenderAgeTransformer()
        output_image_bytes = transformer.transform(image_bytes, selected_attrs)
        response = make_response(output_image_bytes)
        response.headers.set('Content-Type', 'image/jpeg')
        return response
    except SystemError as err:
        print(err)
        return 'Internal Server Error', 500
    except ValueError as value_error:
        return value_error.args[0], 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
