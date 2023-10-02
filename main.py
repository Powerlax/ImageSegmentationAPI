from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('pets')

app = Flask(__name__)

@app.route('/', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        x = jsonify({})
        x.headers.add_header('Access-Control-Allow-Origin', '*')
        x.headers.add_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        x.headers.add_header('Access-Control-Allow-Headers', 'Content-Type')
        return x, 200
    if request.method == 'POST':
        image = request.get_json()
        if image is None:
            response = jsonify({'error': 'Image not provided', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type'})
            return response, 400
        image = image.get('image')
        print("hi")
        pred_mask = model.predict(image)
        pred_mask = np.argmax(pred_mask, axis=-1)
        pred_mask = pred_mask[..., np.newaxis]
        pred_mask_json = pred_mask[0].tolist()
        response = {'new_image': pred_mask_json}
        response = jsonify(response)
        response.headers.add_header('Access-Control-Allow-Origin', '*')
        response.headers.add_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add_header('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200