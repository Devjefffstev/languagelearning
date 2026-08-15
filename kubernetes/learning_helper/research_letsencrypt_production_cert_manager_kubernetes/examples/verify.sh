#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-tls-demo}"
CERTIFICATE_NAME="${CERTIFICATE_NAME:-your-domain-example}"
TLS_SECRET_NAME="${TLS_SECRET_NAME:-your-domain-example-tls}"
ISSUER_NAME="${ISSUER_NAME:-letsencrypt-staging-namecheap}"

kubectl get clusterissuer "$ISSUER_NAME" -o wide
kubectl describe clusterissuer "$ISSUER_NAME"
printf '\nResources:\n'
kubectl get certificate,certificaterequest,order,challenge -n "$NAMESPACE"
printf '\nCertificate details:\n'
kubectl describe certificate "$CERTIFICATE_NAME" -n "$NAMESPACE"
printf '\nNamecheap credential Secret metadata only:\n'
kubectl get secret namecheap-credentials -n "$NAMESPACE"
printf '\nTLS Secret metadata:\n'
kubectl get secret "$TLS_SECRET_NAME" -n "$NAMESPACE"

if command -v openssl >/dev/null 2>&1; then
  echo
  echo "Issued certificate fields:"
  if base64 -D </dev/null >/dev/null 2>&1; then
    DECODER=(base64 -D)
  else
    DECODER=(base64 --decode)
  fi
  kubectl get secret "$TLS_SECRET_NAME" -n "$NAMESPACE" \
    -o jsonpath='{.data.tls\.crt}' \
    | "${DECODER[@]}" \
    | openssl x509 -noout -subject -issuer -dates -ext subjectAltName
else
  echo "openssl is not installed; skipped certificate SAN inspection."
fi
