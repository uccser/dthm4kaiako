#!/bin/bash

source ./infrastructure/dev-deploy/load-dev-deploy-config-envs.sh

# Updates the database for the development system
cp ./infrastructure/cloud-sql-proxy/docker-compose.yml ./docker-compose.yml

# Decrypt secret files archive that contain credentials.
./infrastructure/dev-deploy/decrypt-dev-secrets.sh

# Load environment variables.
source ./dthm4kaiako/load-dev-envs.sh

# Override Elasticsearch connection name for accessing from Travis
export ELASTICSEARCH_CONNECTION_NAME="$DEV_ELASTICSEARCH_CONNECTION_NAME"

# Update the database and website sample content
./dev start
./dev migrate
./dev sampledata
./dev load_achievement_objectives
