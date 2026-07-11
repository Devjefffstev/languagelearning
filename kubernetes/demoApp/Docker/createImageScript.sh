#!bin/bash
# run this script to build the Docker image for the FastAPI application
# Make sure you have Docker installed and running
# Run from the same directory as this script
docker build -t cosmoincorp/demo:my-fastapi-app -f testAPI/Dockerfile testAPI/
docker build -t cosmoincorp/demo:fronted-app -f frontendApp/Dockerfile frontendApp/

docker push cosmoincorp/demo:my-fastapi-app
docker push cosmoincorp/demo:fronted-app

# # Push the images to the local registry
# # Make sure the local registry is running. Run in your terminal createYourOwnLocalDockerRegistry.sh first
#  docker tag my-fastapi-app 10.0.0.100:5000/my-fastapi-app
#  docker push 10.0.0.100:5000/my-fastapi-app

# docker tag fronted-app localhost:5000/fronted-app
# docker push localhost:5000/fronted-app

# # List the images in the local registry to verify
# docker exec local-registry /bin/sh -c 'tree /var/lib/registry'