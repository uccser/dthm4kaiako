#!/bin/bash

# Decrypt secret files archive that contain credentials.
#
# This includes:
#   - Google Cloud Platform Service Account for using gcloud.
#   - Script tp load environment variables used for running Django in production.
openssl aes-256-cbc -K "${encrypted_adab45d1d2ed_key}" -iv "${encrypted_adab45d1d2ed_iv}" -in ./infrastructure/prod-deploy/prod-deploy-secrets.tar.enc -out prod-deploy-secrets.tar -d

# Unzip the decrypted secret archive.
tar -C ./dthm4kaiako/dthm4kaiako/ -xf prod-deploy-secrets.tar
