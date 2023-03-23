import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import os
from flask import Flask, request
from werkzeug.utils import secure_filename

# instance text detector
reader = easyocr.Reader(['es'], gpu=False)
UPLOAD_FOLDER = os.getcwd() + "\\img\\uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# init flask
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/analyze", methods=['POST'])
def analyze():
    image = request.files['file']

    if not image:
        return 'No image uploaded', 400
    
    if image and allowed_file(image.filename):
            list = []
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            img = cv2.imread(image_path)

            # detect text on image
            text_ = reader.readtext(img)

            # draw bbox and text
            for t in text_:
                list.append(t[1])
            # bbox, text, score = t
            print(list)
            return list