# import the necessary packages
import os
import sys
import requests
import ssl
from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file

from uuid import uuid4

from os import path

from color_transfer import color_transfer
import cv2
import numpy as np

from pathlib import Path
import traceback


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def download(url, filename):
    data = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(data)

    return filename


def generate_random_filename(extension):
    filename = str(uuid4())
    filename = os.path.join(upload_directory, filename + "." + extension)
    return filename


def clean_me(filename):
    if os.path.exists(filename):
        os.remove(filename)


def clean_all(files):
    for me in files:
        clean_me(me)


@app.route("/process", methods=["POST"])
def process_image():

    source_filename = generate_random_filename("jpg")
    target_filename = generate_random_filename("jpg")
    output_filename = generate_random_filename("jpg")
        
    try:
        if 'source' in request.files:
            source = request.files['source']
            if allowed_file(source.filename):
                source.save(source_filename)
        if 'target' in request.files:
            target = request.files['target']
            if allowed_file(target.filename):
                target.save(target)
            
        else:
            url = request.json["url"]
            download(url, input_path)
            source_url = request.json["source_url"]
            target_url = request.json["target_url"]

            source_filename = download(source_url, source_filename) 
            target_filename = download(target_url, target_filename) 

        source = cv2.imread(source_filename)
        target = cv2.imread(target_filename)

        transfer = color_transfer(
            source, 
            target, 
            clip=True, 
            preserve_paper=True
            )

        cv2.imwrite(target_filename, transfer)
        callback = send_file(target_filename, mimetype='image/jpeg')
        
        return callback, 200

    except:
        traceback.print_exc()
        return {'message': 'input error'}, 400

    finally:
        clean_all([
            source_filename, 
            target_filename, 
            output_filename
            ])


if __name__ == '__main__':
    global upload_directory
    global ALLOWED_EXTENSIONS
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    
    upload_directory = 'upload'

    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    port = 5000
    host = '0.0.0.0'

    app.run(host=host, port=port, threaded=True)
