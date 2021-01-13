import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Some utilites
import numpy as np
from util import base64_to_pil


from src.infer import infer_step
import os
from datetime import datetime
import argparse
import textwrap
import time


# Declare a flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# You can use pretrained model from Keras
# Check https://keras.io/applications/
# or https://www.tensorflow.org/api_docs/python/tf/keras/applications

import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')



# Model saved with Keras model.save()
MODEL_PATH = 'data/model.pkl'

# Load your own trained model
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')




@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print(request.json)
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        img.save("data/flask/image.png")

        try:
            start = time.time()
            infer_step(fname_infer=os.path.join("data", 'flask'),
                       fname_save=os.path.join("result", 'flask'),
                       fname_model=os.path.join("data", 'model.pkl'),
                       thre_discard=100, wid_dilate=1,
                       fstats=False)
            print("infer time", time.time() - start)
        except Exception as e:
            raise Exception(e, "Got an error in inference step.")

        result = get_base64_encoded_image('result/flask/image.png')
        
        # Serialize the result, you can add additional fields
        return jsonify(result=result)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
