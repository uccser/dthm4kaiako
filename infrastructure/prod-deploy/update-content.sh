#!/bin/bash

source ./infrastructure/prod-deploy/load-prod-deploy-config-envs.sh

# Updates the database for the development system
cp ./infrastructure/cloud-sql-proxy/docker-compose.yml ./docker-compose.yml

# Decrypt secret files archive that contain credentials.
./infrastructure/prod-deploy/decrypt-prod-secrets.sh

# Load environment variables.
source ./dthm4kaiako/load-prod-envs.sh

# Override Elasticsearch connection name for accessing from Travis
export ELASTICSEARCH_CONNECTION_NAME="$PROD_ELASTICSEARCH_CONNECTION_NAME"

# Start the system and run the migrate and collect_static system commands.
./dev start
./dev migrate
./dev load_card_data
./dev load_poet_data
