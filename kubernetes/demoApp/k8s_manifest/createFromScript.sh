#to create deployment 
kubectl create namespace demo-app
# to create deployment for the FastAPI application
# Make sure you have the Docker image built and available in your local Docker registry
# or in a remote registry accessible by your Kubernetes cluster
# Ensure the Docker image is built with the correct tag
kubectl create deployment test-api --namespace=demo-app --image=localhost:5000/my-fastapi-app:latest --replicas=2 
