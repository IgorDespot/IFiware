#!/bin/bash
# Stop all containers
docker stop $(docker ps -a -q)
# Delete all containers
docker rm $(docker ps -a -q)
# Delete all images
docker rmi $(docker images -q)
sudo rm -r data
sudo docker system prune -a
sudo docker volume prune 

