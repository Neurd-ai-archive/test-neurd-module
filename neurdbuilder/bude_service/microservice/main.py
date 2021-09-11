import os
import base64
import shutil
import subprocess
import time
import zipfile
from flask import Flask, request
try:
  import googleclouddebugger
  googleclouddebugger.enable(
    breakpoint_enable_canary=True
  )

except ImportError:
  pass

app = Flask(__name__)
proj = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True).stdout.decode("utf-8").strip("\n")
ti = int(time.time())
targ = f"gcr.io/{proj}/{ti}"

# folders for files:
ZIP = "ZIP/"
BUILD = "BUILD/"

def build_and_deploy():
    out = "building\n\n\n"
    gcloud_build = subprocess.run(["gcloud", "builds", "submit", BUILD, "--tag", f"{targ}"], capture_output=True)

    if gcloud_build.stdout.decode("utf-8") != "":
        out += gcloud_build.stdout.decode("utf-8")
    else:
        out += gcloud_build.stderr.decode("utf-8")

    out += "finished building\n\n\ndeploying\n\n\n"

    gcloud_deploy = subprocess.run(["gcloud", "run", "deploy", f"web-{ti}", "--image", f"{targ}", "--allow-unauthenticated", "--region=europe-central2"], capture_output=True)
    if gcloud_deploy.stdout.decode("utf-8") != "":
        out += gcloud_deploy.stdout.decode("utf-8")
    else:
        out += gcloud_deploy.stderr.decode("utf-8")
    return out

def unzip_to_dir(zip, target_dir):
    with zipfile.ZipFile(zip, "r") as z:
        z.extractall(target_dir)

def clean_up_files(folder):
 for filename in os.listdir(folder):
     file_path = os.path.join(folder, filename)
     try:
         if os.path.isfile(file_path) or os.path.islink(file_path):
             os.unlink(file_path)
         elif os.path.isdir(file_path):
             shutil.rmtree(file_path)
     except Exception as e:
         print('Failed to delete %s. Reason: %s' % (file_path, e))



@app.route("/")
def index():
    return "to build and deploy a service please send a zip of your buildfiles via post to /rec"

@app.route("/rec", methods=["POST"])
def rec():
    # receive files
    raw_request = request.get_json()
    if raw_request['type'] == "data":
        with open(ZIP+"received.zip", "wb") as f:
            # encode the received bytes as utf-8, then decode the base64 encoded strings
            decoded = base64.decodebytes(raw_request["data"].encode("utf-8"))
            # write to received.zip
            f.write(decoded)
    else:
        return "No data received!"

    # unzip files
    unzip_to_dir(ZIP+"received.zip", BUILD)

    # build and deploy
    # return output to user
    out = build_and_deploy()

    # clean_up_files(ZIP)
    # clean_up_files(BUILD)

    return out


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
