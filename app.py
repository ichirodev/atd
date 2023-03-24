import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from util.text import clean_string, find_route, find_concentration
from medicament import MedicamentPackage

reader = easyocr.Reader(['es'], gpu=True)
UPLOAD_FOLDER = os.getcwd() + "\\img\\uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            img = cv2.imread(image_path)
            detected_text = reader.readtext(img)

            text_list = []
            for text_line in detected_text:
                text = clean_string(text_line[1]).upper()
                if text != "":
                    text_list.append(text)
            
            concentration, text_list = find_concentration(text_list)
            route, text_list = find_route(text_list)
            medicament = "Diclofenaco" # get data from scrapper, then search this name into the db
            purpose = "Inflamacion" # get purpose of medicament

            medicament = MedicamentPackage("Diclofenaco", concentration, route, "Inflamacion")
        
            return medicament.json()