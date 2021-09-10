import os
import base64
from flask import Flask, request, jsonify
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join


app = Flask(__name__)

# checks if dir exists, if not creates it
def check_or_make_dir(path):
    if not os.path.exists(path):
         os.makedirs(path)


@app.route('/post', methods=["POST"])
def receive():
    # get the json data from the post request
    data = request.get_json()
    # check if the type is data
    if data['type'] == "data":
        with open("received.zip", "wb") as f:
            # encode the received bytes as utf-8, then decode the base64 encoded strings
            decoded = base64.decodebytes(data["data"].encode("utf-8"))
            # write to received.zip
            f.write(decoded)
    else:
        print("no data")

    return "Received"

if __name__ == "__main__":
    app.run(debug=True, port=8080)
