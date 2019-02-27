#!/bin/bash

source ./infrastructure/prod-deploy/load-prod-deploy-config-envs.sh

# Updates the database for the development system
cp ./infrastructure/cloud-sql-proxy/docker-compose.yml ./docker-compose.yml

# Decrypt secret files archive that contain credentials.
./infrastructure/prod-deploy/decrypt-prod-secrets.sh
ls ./dthm4kaiako/

# Load environment variables.
source ./dthm4kaiako/load-prod-envs.sh

# Start the system and run the migrate and collect_static system commands.
./dev start
./dev migrate
