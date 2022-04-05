#!/bin/bash

set -e

# Check for environment variables
checkEnvVariableExists() {
    if [ -z ${!1} ]
    then
        echo "ERROR: Define $1 environment variable."
        exit 1
    else
        echo "INFO: $1 environment variable found."
    fi
}
checkEnvVariableExists DTHM4KAIAKO_IMAGE_TAG
checkEnvVariableExists DTHM4KAIAKO_ROUTER_RULE

# Update Django service
docker stack deploy dthm4kaiako -c docker-compose.prod.yml

# Wait until previous command finishes
docker service scale dthm4kaiako_task-update-data=1
