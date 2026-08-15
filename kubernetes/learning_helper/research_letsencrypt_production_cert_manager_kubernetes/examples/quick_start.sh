#!/usr/bin/env bash
set -euo pipefail

# Quick staging-only path. Requires cert-manager and the Namecheap webhook
# chart to already be installed in the cluster.
: "${DOMAIN:?Set DOMAIN, for example DOMAIN=example.com}"
: "${ACME_EMAIL:?Set ACME_EMAIL}"
: "${NAMECHEAP_API_KEY:?Set NAMECHEAP_API_KEY}"
: "${NAMECHEAP_API_USER:?Set NAMECHEAP_API_USER}"
: "${NAMECHEAP_CLIENT_IP:?Set NAMECHEAP_CLIENT_IP to the whitelisted public IPv4}"

NAMESPACE="${NAMESPACE:-tls-demo}"
CERTIFICATE_NAME="${CERTIFICATE_NAME:-${DOMAIN//./-}-staging}"
TLS_SECRET_NAME="${TLS_SECRET_NAME:-${DOMAIN//./-}-staging-tls}"

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# The webhook reads this Secret from the Certificate's namespace.
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
  name: "$CERTIFICATE_NAME"
  namespace: "$NAMESPACE"
spec:
  secretName: "$TLS_SECRET_NAME"
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

echo "Waiting for staging Certificate/$CERTIFICATE_NAME in namespace $NAMESPACE..."
kubectl wait --for=condition=Ready "certificate/$CERTIFICATE_NAME" \
  -n "$NAMESPACE" --timeout=15m

echo
echo "Staging certificate is Ready. Inspect the flow with:"
echo "  kubectl get certificate,certificaterequest,order,challenge -n $NAMESPACE"
echo "  kubectl get secret $TLS_SECRET_NAME -n $NAMESPACE"
echo
echo "Do not use this staging certificate for normal browser traffic."
echo "After reviewing the result, use complete_setup.sh with PROMOTE_TO_PRODUCTION=true."
