#importing libraries for api building 
import pytesseract
from PIL import Image
import sys
import cv2
import numpy as np
import sys
import json
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api

#importing necessary functions
from main import *

#initializing API
app = Flask(__name__)
api = Api(app)

#defining the path 
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#getting the image and identifying details using the function and returning in JSON format
@app.route('/driving',methods = ['POST'])
def dl_details():
    file = request.files['image']
    img = Image.open(file.stream)
    dl_details = get_details(img)
    return(jsonify(dl_details))

if __name__ == "__main__":
    app.run(debug=True)
