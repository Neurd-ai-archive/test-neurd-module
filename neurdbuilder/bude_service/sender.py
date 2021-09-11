import os
import argparse
import requests
import json
import base64
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile


# https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
def zip_folder(base_path, filename="sampleDir.zip"):
    # create a ZipFile object
    with ZipFile(filename, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(base_path):
           for f in filenames:
               #create complete filepath of file in directory
               filePath = os.path.join(folderName, f)
               # Add file to zip
               zipObj.write(filePath, os.path.basename(filePath))
    return filename

# base64 encodes a given file
def encode_zip(filename):
    return base64.b64encode(open(filename, "rb").read()).decode("utf-8")

def send_files(base_path, addr):
    # ztip the files in the given folder
    filename = zip_folder(base_path)
    # base64 encode them 
    b64 = encode_zip(filename)
    json_data = {"type": "data", "data": b64}
    # send b64 as post request
    r = requests.post(addr, json=json_data)
    print(r.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path" )
    parser.add_argument("-a", "--address")
    args = parser.parse_args()

    send_files(args.path, args.address)


