# Minikube & Ingress NGINX Controller Manual Installation Guide

This guide explains how to install Minikube and manually set up the Ingress NGINX controller for local Kubernetes development.

---

## 1. Install Minikube

### Prerequisites

- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed  
  <br>**If you see `Command 'kubectl' not found, but can be installed with:`**  
  Install it using:
  ```sh
  sudo snap install kubectl --classic
  ```
  Or follow the [official instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/).
- Virtualization enabled (e.g., VirtualBox, KVM, Hyper-V, Docker)

### Installation

#### Linux

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## 2. Install a Minikube Driver

Minikube requires a driver to run Kubernetes nodes. You must install one of the following drivers:

- **Docker** (recommended for most users)
- **KVM2** (for Linux)
- **Podman**
- **QEMU2**
- **VirtualBox**

### Example: Install Docker (Recommended)

```sh
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

Or, for KVM2:

```sh
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo usermod -aG libvirt $USER
newgrp libvirt
```

For more drivers and troubleshooting, see [Minikube Drivers](https://minikube.sigs.k8s.io/docs/drivers/).

---

## 3. Start Minikube

To allow Minikube to use most of your system's CPU cores and memory, but leave enough for system overhead, follow these steps:

First, check your system resources:

```sh
nproc        # Shows number of CPU cores
free -h      # Shows available memory
```

**Important:**  
Do **not** allocate all available memory to Minikube. Leave at least 2–4 GB for your operating system to avoid stability issues.

For example, if your system has 16 GB RAM, allocate around 12–14 GB to Minikube:

```sh
minikube start --driver=docker --cpus=$(nproc) --memory=14000mb
```

If you get a warning about memory allocation, reduce the value as suggested by Minikube (e.g., `--memory=3900mb`).

> **Note:**  
> If you want to change the CPU or memory allocation for an existing Minikube cluster, you must first delete the cluster:
>
> ```sh
> minikube delete
> ```

Replace `docker` with your installed driver if different.

---

## 4. Enable Ingress NGINX Controller

### Option 1: Minikube Addon

```sh
minikube addons enable ingress
```

### Option 2: Manual Installation

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml
kubectl get pods -n ingress-nginx
```

---

## 5. Verify Installation

Check that the ingress controller pod is running:

```sh
kubectl get pods -n ingress-nginx
```

---

## How to Access the Ingress Controller from the Internet

By default, Minikube and its Ingress controller are only accessible from your local machine. To expose the Ingress controller to the internet, follow these steps:

### 1. Expose the Ingress Controller Service

First, check the service type for the ingress controller:

```sh
kubectl get svc -n ingress-nginx
```

Look for a service named `ingress-nginx-controller`. By default, it is of type `ClusterIP` or `NodePort`.

#### Change Service to LoadBalancer (Recommended for Cloud VMs)

If you are running Minikube on a cloud VM (with a public IP), you can patch the service to type `LoadBalancer`:

```sh
kubectl patch svc ingress-nginx-controller -n ingress-nginx -p '{"spec": {"type": "LoadBalancer"}}'
```

Wait a few seconds, then get the external IP:

```sh
kubectl get svc -n ingress-nginx
```

The `EXTERNAL-IP` column should show your VM's public IP.

### 2. (Alternative) Use NodePort

If `LoadBalancer` is not available, use `NodePort` and access via your VM's public IP and the assigned port:

```sh
kubectl patch svc ingress-nginx-controller -n ingress-nginx -p '{"spec": {"type": "NodePort"}}'
kubectl get svc -n ingress-nginx
```

Find the `NODE-PORT` (e.g., 30080). Access your ingress like this:

```
http://<your-vm-public-ip>:<node-port>
```

### 3. Update DNS (Optional)

If you want to use a domain name, create a DNS A record pointing to your VM's public IP.

### 4. Firewall Rules

Make sure your VM's firewall allows inbound traffic on the required port (80/443 for HTTP/HTTPS, or the NodePort you found).

**Example for Ubuntu UFW:**

```sh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
# Or for NodePort, e.g., 30080
sudo ufw allow 30080/tcp
```

---

**Note:**  
Exposing Minikube to the internet is not recommended for production. Use this only for testing or development, and secure your cluster appropriately.

---

## 5. Troubleshooting: EXTERNAL-IP is `<pending>`

When you patch the ingress controller service to `LoadBalancer` on a cloud VM, you may see:

```
ingress-nginx-controller   LoadBalancer   10.106.212.81   <pending>   80:32694/TCP,443:31555/TCP   ...
```

This happens because Minikube does not automatically provision an external IP for LoadBalancer services. To access your ingress from the internet, you need to manually assign your VM's public IP.

#### Solution: Manually Set the External IP

1. **Edit the Service:**
   ```sh
   kubectl edit svc ingress-nginx-controller -n ingress-nginx
   ```
2. In the editor, under `spec:`, add your VM's public IP as an `externalIPs` entry. For example:
   ```yaml
   spec:
     type: LoadBalancer
     externalIPs:
       - <your-vm-public-ip>
   ```
   Replace `<your-vm-public-ip>` with your actual public IP address.

3. **Save and exit** the editor.

4. **Verify:**
   ```sh
   kubectl get svc -n ingress-nginx
   ```
   The `EXTERNAL-IP` column should now show your public IP.

5. **Access your ingress:**
   - Use `http://<your-vm-public-ip>` or `https://<your-vm-public-ip>` in your browser or API client.

---

**Note:**  
If you use NodePort instead, access your ingress at `http://<your-vm-public-ip>:<node-port>`.

---

## References

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Ingress NGINX Controller](https://kubernetes.github.io/ingress-nginx/)