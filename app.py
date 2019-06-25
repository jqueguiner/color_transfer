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


def download(url, filename):
    data = requests.get(url).content
    with open(filename, 'wb') as handler:
        handler.write(data)

    return filename


@app.route("/process", methods=["POST"])
def process_image():

    source_filename = str(uuid4())
    source_filename = os.path.join(directory, source_filename + ".jpg")

    target_filename = str(uuid4())
    target_filename = os.path.join(directory, target_filename + ".jpg")
        
    try:
        source_url = request.json["source_url"]
        target_url = request.json["target_url"]

        source_filename = image(source_url, source_filename) 
        target_filename = image(source_url, target_filename) 

        source = cv2.imread(source_filename)
        target = cv2.imread(target_filename)

        transfer = color_transfer(
            source, 
            target, 
            clip=True, 
            preserve_paper=True
            )

        cv2.imwrite(source_filename, transfer)
        callback = send_file(source_filename, mimetype='image/jpeg')
        
        return callback, 200

    except:
        traceback.print_exc()
        return {'message': 'input error'}, 400

    finally:
        if os.path.exists(source_filename)):
            os.remove(source_filename)

        if os.path.exists(target_filename):
            os.remove(target_filename)


if __name__ == '__main__':
    global upload_directory
    
    upload_directory = 'upload'

    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    port = 5000
    host = '0.0.0.0'

    app.run(host=host, port=port, threaded=True)
