import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import os
import difflib
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from util.text import clean_string, find_first, find_concentration, filter_text
from medicament import MedicamentPackage
from util.dictionary import load_dictionary
from flask_cors import CORS

CURRENT_PATH = os.getcwd()
UPLOAD_FOLDER = CURRENT_PATH + "\\img\\uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

reader = easyocr.Reader(['es'], gpu=True)

bloat_dictionary = load_dictionary(CURRENT_PATH + "\\bloat_dictionary.txt")
route_dictionary = load_dictionary(CURRENT_PATH + "\\route_dictionary.txt")

db_connection = mysql.connector.connect(
        host = "100.81.187.129",
        user = "mm",
        password = "passw0rd",
        database = "drugdb",
        port = "3306"
    )
db_cursor = db_connection.cursor()

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_drug_on_db(cursor, drug):
    query = "SELECT name, purpose FROM drugdb.drug WHERE name = '{}' OR name LIKE '%{}%' ORDER BY name ASC".format(drug, drug)
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        i = 0
        names = []

        for i in range(0, len(data)):
            names.append(data[i][0])
            if data[i][0] == drug:
                return data[i][0], data[i][1]
    
        close_matches = difflib.get_close_matches(drug, names)
        if len(close_matches) > 0:
            closer_match_index = names.index(close_matches[0])
            return data[closer_match_index][0], data[closer_match_index][1]
        
        if len(data) > 0:
            return data[0][0], data[0][1] or ""
    except mysql.connector.Error as err:
        print("Failed to fetch", drug, "from the DB", err)
    return None, ""

def get_data_from_list(cursor, list):
    for item in list:
        drug_name, drug_purpose = find_drug_on_db(cursor, item)
        if drug_name is not None:
             return drug_name, drug_purpose
    return drug_name, drug_purpose
     
@app.route('/')
def heartbeat():
    return '{"status": "okay"}'

@app.route("/api/analyze", methods=['POST'])
def analyze():
    print("Image detected")
    image = request.files['image']

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
            route, text_list = find_first(text_list, route_dictionary)
            text_list = filter_text(text_list, bloat_dictionary)
            text_list = filter_text(text_list, route_dictionary)
            medicament, purpose = get_data_from_list(db_cursor, text_list)

            medicament = MedicamentPackage(medicament, concentration, route, purpose)

            return medicament.json()
