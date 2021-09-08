#!/bin/bash

PROJ=$(gcloud config get-value project)
TS=$(date +%s)
TARG=gcr.io/$PROJ/$TS

cd deploy
gcloud builds submit --tag $TARG > ../log.txt
gcloud run deploy $TS-web --image $TARGET --allow-unauthenticated --region=europe-central2 | grep "Service"
