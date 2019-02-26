#!/bin/bash

# Decrypt secret files archive that contain credentials.
#
# This includes:
#   - Google Cloud Platform Service Account for using gcloud.
#   - Script tp load environment variables used for running Django on development server.
openssl aes-256-cbc -K "${encrypted_22a91f07bb63_key}" -iv "${encrypted_22a91f07bb63_iv}" -in ./infrastructure/dev-deploy/dev-deploy-secrets.tar.enc -out ./dthm4kaiako/dev-deploy-secrets.tar -d

# Unzip the decrypted secret archive.
tar -C ./dthm4kaiako/ -xf ./dthm4kaiako/dev-deploy-secrets.tar
