import os
from flask import Flask
import subprocess
import time

app = Flask(__name__)
proj = subprocess.check_output(["gcloud config get-value project"], shell=True).decode("utf-8").strip("\n")
ti = int(time.time())
targ = f"gcr.io/{proj}/{ti}"


@app.route("/")
def index():
    return "to build and deploy a hello world container please visit /build and then /deploy"

@app.route("/build")
def build():
    out = subprocess.check_output([f"gcloud builds submit deploy/ --tag {targ}"], shell=True).decode("utf-8")
    return out

@app.route("/deploy")
def deploy():
    out = subprocess.check_output([f"gcloud run deploy web-{ti} --image {targ} --allow-unauthenticated --region=europe-central2"], shell=True).decode("utf-8")
    return out


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
