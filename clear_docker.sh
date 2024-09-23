#!/bin/bash

# Stop all running containers
docker stop $(docker ps -a -q)

# Remove all stopped containers
docker rm $(docker ps -a -q)

# Remove   
 all images
docker rmi $(docker images -q)

# Remove all networks
docker network rm $(docker network ls -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)