# Neurdbuilder Microservice

- when deployed, service listens on /rec for incoming post requests
    - post request contains json file with b64 encoded zip file of files to build 
- neurdbuilder builds image and deploys it to gcr.io
