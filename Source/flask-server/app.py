from flask import Flask, request, make_response
from transformation import HaircolorGenderAgeTransformer

app = Flask(__name__)


@app.route('/haircolor-gender-age', methods=['POST'])
def haircolor_gender_age_transformer():
    image_bytes = request.get_data()
    attrs = request.args.getlist('attrs[]')

    if len(attrs) == 0:
        attrs = request.args.getlist('attrs')

    if len(attrs) == 0:
        return 'Request must include param \'attrs\'', 400

    print(attrs)

    try:
        transformer = HaircolorGenderAgeTransformer()
        output_image_bytes = transformer.transform(image_bytes, attrs)
        response = make_response(output_image_bytes)
        response.headers.set('Content-Type', 'image/jpeg')
        return response
    except SystemError as err:
        print(err)
        return 'Internal Server Error', 500
    except ValueError as value_error:
        return value_error.args[0], 400


if __name__ == '__main__':
    app.run(debug=True)
