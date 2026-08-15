#!/usr/bin/env bash
set -euo pipefail

# Complete, gated setup. It installs cert-manager and the referenced Namecheap
# webhook, issues a staging certificate, and only then can optionally issue a
# separate production certificate.
: "${DOMAIN:?Set DOMAIN, for example DOMAIN=example.com}"
: "${ACME_EMAIL:?Set ACME_EMAIL}"
: "${NAMECHEAP_API_KEY:?Set NAMECHEAP_API_KEY}"
: "${NAMECHEAP_API_USER:?Set NAMECHEAP_API_USER}"
: "${NAMECHEAP_CLIENT_IP:?Set NAMECHEAP_CLIENT_IP to the whitelisted public IPv4}"

NAMESPACE="${NAMESPACE:-tls-demo}"
CERT_MANAGER_VERSION="${CERT_MANAGER_VERSION:-v1.21.0}"
WEBHOOK_TAG="${WEBHOOK_TAG:-cert-manager-webhook-namecheap-0.2.2}"
WEBHOOK_DIR="${WEBHOOK_DIR:-.cache/cert-manager-webhook-namecheap}"
PROMOTE_TO_PRODUCTION="${PROMOTE_TO_PRODUCTION:-false}"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl is required" >&2
  exit 1
fi
if ! command -v helm >/dev/null 2>&1; then
  echo "Helm 3 is required" >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "git is required to fetch the webhook source" >&2
  exit 1
fi

helm upgrade --install cert-manager \
  oci://quay.io/jetstack/charts/cert-manager \
  --version "$CERT_MANAGER_VERSION" \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true

kubectl rollout status deployment/cert-manager -n cert-manager --timeout=5m
kubectl rollout status deployment/cert-manager-webhook -n cert-manager --timeout=5m

if [ ! -d "$WEBHOOK_DIR/.git" ]; then
  mkdir -p "$(dirname "$WEBHOOK_DIR")"
  git clone --branch "$WEBHOOK_TAG" --depth 1 \
    https://github.com/Extrality/cert-manager-webhook-namecheap.git \
    "$WEBHOOK_DIR"
fi

# This project is archived and unsupported. Pin the source tag, inspect it,
# and replace this dependency with a maintained fork or supported provider
# before using the pattern for production.
helm upgrade --install namecheap-webhook \
  "$WEBHOOK_DIR/charts/cert-manager-webhook-namecheap" \
  --namespace cert-manager \
  --set certManager.namespace=cert-manager \
  --set certManager.serviceAccountName=cert-manager \
  --set groupName=acme.namecheap.com \
  --set replicaCount=1 \
  --set image.tag=v0.3.1

kubectl rollout status deployment/namecheap-webhook-cert-manager-webhook-namecheap \
  -n cert-manager --timeout=5m

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
kubectl -n "$NAMESPACE" create secret generic namecheap-credentials \
  --from-literal=apiKey="$NAMECHEAP_API_KEY" \
  --from-literal=apiUser="$NAMECHEAP_API_USER" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -f - <<YAML
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging-namecheap
spec:
  acme:
    email: "$ACME_EMAIL"
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-staging-namecheap-account-key
    solvers:
      - dns01:
          webhook:
            groupName: acme.namecheap.com
            solverName: namecheap
            config:
              apiKeySecretRef:
                name: namecheap-credentials
                key: apiKey
              apiUserSecretRef:
                name: namecheap-credentials
                key: apiUser
              clientIP: "$NAMECHEAP_CLIENT_IP"
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ${DOMAIN//./-}-staging
  namespace: "$NAMESPACE"
spec:
  secretName: ${DOMAIN//./-}-staging-tls
  duration: 2160h
  renewBefore: 360h
  privateKey:
    rotationPolicy: Always
  dnsNames:
    - "$DOMAIN"
    - "www.$DOMAIN"
    - "*.$DOMAIN"
  issuerRef:
    name: letsencrypt-staging-namecheap
    kind: ClusterIssuer
    group: cert-manager.io
YAML

STAGING_CERTIFICATE="${DOMAIN//./-}-staging"
kubectl wait --for=condition=Ready "certificate/$STAGING_CERTIFICATE" \
  -n "$NAMESPACE" --timeout=15m

echo "Staging certificate is Ready. Staging roots are not trusted by normal browsers."
echo "Review DNS cleanup, SANs, webhook logs, and the generated Secret before promotion."

if [ "$PROMOTE_TO_PRODUCTION" != "true" ]; then
  echo "Production promotion is gated. Re-run with PROMOTE_TO_PRODUCTION=true after review."
  exit 0
fi

kubectl apply -f - <<YAML
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod-namecheap
spec:
  acme:
    email: "$ACME_EMAIL"
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod-namecheap-account-key
    solvers:
      - dns01:
          webhook:
            groupName: acme.namecheap.com
            solverName: namecheap
            config:
              apiKeySecretRef:
                name: namecheap-credentials
                key: apiKey
              apiUserSecretRef:
                name: namecheap-credentials
                key: apiUser
              clientIP: "$NAMECHEAP_CLIENT_IP"
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ${DOMAIN//./-}-production
  namespace: "$NAMESPACE"
spec:
  secretName: ${DOMAIN//./-}-production-tls
  duration: 2160h
  renewBefore: 360h
  privateKey:
    rotationPolicy: Always
  dnsNames:
    - "$DOMAIN"
    - "www.$DOMAIN"
    - "*.$DOMAIN"
  issuerRef:
    name: letsencrypt-prod-namecheap
    kind: ClusterIssuer
    group: cert-manager.io
YAML

PRODUCTION_CERTIFICATE="${DOMAIN//./-}-production"
kubectl wait --for=condition=Ready "certificate/$PRODUCTION_CERTIFICATE" \
  -n "$NAMESPACE" --timeout=15m

echo "Production certificate is Ready in Secret ${DOMAIN//./-}-production-tls."
echo "Update the Ingress or Gateway to reference that Secret, then verify with a normal client."
