# https://k21academy.com/docker-kubernetes/how-to-set-up-your-own-local-docker-registry-a-step-by-step-guide/
#!/bin/bash
# run this script to create a local Docker registry
# Make sure you have Docker installed and running
docker run -d -p 5000:5000 --name local-registry registry:2
docker container ls
docker exec local-registry /bin/sh -c 'ls /var/lib/registry'  

# If you give this error 
# Failed to pull image "10.0.0.100:5000/my-fastapi-app:latest": failed to pull and unpack image "10.0.0.100:5000/my-fastapi-app:latest": failed to resolve reference "10.0.0.100:5000/my-fastapi-app:latest": failed to do request: Head "https://10.0.0.100:5000/v2/my-fastapi-app/manifests/latest": http: server gave HTTP response to HTTPS client
# you need to add the insecure registry to the Docker daemon configuration
# Edit the Docker daemon configuration file
# sudo nano /etc/docker/daemon.json
# Add the following content to the file
# {
#   "insecure-registries": ["localhost:5000"]
# }
# Restart the Docker service to apply the changes
# sudo systemctl restart docker
# After restarting the Docker service, you can verify that the local registry is accessible
# by running the following command
# docker pull localhost:5000/my-fastapi-app:latest
# If you got the error 
# Error response from daemon: Get "http://localhost:5000/v2/": dial tcp 127.0.0.1:5000: connect: connection refused
# you need to check if the local registry is running
# by running the following command
# docker container ls
# If the local registry is not running, you can start it by running the following command
# docker start local-registry
#
# If you have more workers in your Kubernetes cluster, you need to make sure that the local registry is accessible from all the workers.
# You can do this by adding the local registry to the Docker daemon configuration on each worker
# and restarting the Docker service on each worker.

# If youre using containerd instead of Docker, you need to add the local registry to the containerd configuration
# Edit the containerd configuration file
# sudo nano /etc/containerd/config.toml
# If the folder /etc/containerd does not exist, you can create it by running the following command
# sudo mkdir -p /etc/containerd

# If the file /etc/containerd/config.toml does not exist, you can create it by running the following command
# sudo -u root containerd config default > /etc/containerd/config.toml

# if you got sudo -u root containerd config default > /etc/containerd/config.toml
#-bash: /etc/containerd/config.toml: Permission denied
# you can run the command with sudo
# sudo sh -c 'containerd config default > /etc/containerd/config.toml'

# sudo systemctl restart containerd

# sudo systemctl enable containerd



# Add the following content to the file

# then after these steps open then file

# sudo nano /etc/containerd/config.toml

# find this line

# [plugins."io.containerd.grpc.v1.cri".registry.configs]

# add these lines below that line

#    [plugins."io.containerd.grpc.v1.cri".registry.configs."registry-ip:5000"]


#    [plugins."io.containerd.grpc.v1.cri".registry.configs."registry-ip:5000".tls] 
#         ca_file = ""
#         cert_file = "" 
#         insecure_skip_verify = true 
#         key_file = ""

# then search this line [plugins."io.containerd.grpc.v1.cri".registry.mirrors]

# and add the below lines below that line

#  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."registry-ip:5000"] 
#           endpoint = ["http://registry-ip:5000"] 

# Restart the containerd service to apply the changes
# sudo systemctl restart containerd
# After restarting the containerd service, you can verify that the local registry is accessible
# by running the following command
# ctr -n k8s.io images pull localhost:5000/my-fastapi-app:latest
# If you got the error
# failed to resolve reference "localhost:5000/my-fastapi-app:latest": failed to do request: Head "http://localhost:5000/v2/my-fastapi-app/manifests/latest": dial tcp
