# Let's Encrypt Production with cert-manager on Kubernetes

## Description

Let's Encrypt is a public Certificate Authority (CA). It issues free TLS certificates through **ACME**, an automated protocol for proving that you control a domain and requesting a certificate. The production ACME directory is `https://acme-v02.api.letsencrypt.org/directory`; certificates from it are trusted by normal browsers and operating systems.

In Kubernetes, **cert-manager** is the controller that turns a desired `Certificate` resource into an actual certificate stored in a Kubernetes `Secret`. It is a Kubernetes-native ACME client. You describe the desired state once, and cert-manager creates the intermediate resources, solves the domain challenge, writes the certificate, and renews it before it expires.

The most useful mental model is: `Certificate` is the request, `ClusterIssuer` is the account and CA connection, `Order` is the CA's certificate order, and `Challenge` is the proof-of-domain-control task. For a Namecheap DNS-01 integration, the webhook writes a temporary TXT record at `_acme-challenge.<domain>` through the Namecheap API. Let's Encrypt checks that TXT record, then cert-manager stores `tls.crt` and `tls.key` in the requested Secret.

This guide focuses on production behavior, SAN certificates, DNS-01, `ClusterIssuer`, renewal, and the staging-first cutover. It intentionally has no exercises. The examples use a third-party Namecheap webhook because Namecheap is not an in-tree cert-manager DNS provider. Treat that webhook as a dependency to audit: the commonly referenced `Extrality/cert-manager-webhook-namecheap` repository is archived and marked unsupported.

**Last verified:** July 27, 2026. Let’s Encrypt endpoints, rate limits, cert-manager releases, and third-party webhook images can change; re-check the linked documentation before a production rollout.

## Analogy

Imagine a company mailroom. A `Certificate` is an employee's request for an official company badge. The `ClusterIssuer` is the mailroom's authorized relationship with the badge office. An ACME `Order` is the badge-office ticket. Each `Challenge` is a question the badge office asks: “Can you place this exact note in a location only the domain owner controls?”

With DNS-01, the note is a TXT record under `_acme-challenge`. The Namecheap webhook is the courier that places and removes the note. After the badge office sees the note, Let's Encrypt signs the badge, cert-manager puts it in a Kubernetes Secret, and the Ingress or Gateway presents it to visitors.

## Examples

### Example #1

#### Quick setup

This quick path assumes cert-manager and the Namecheap webhook are already installed. It creates a staging `ClusterIssuer` and requests one SAN certificate containing the apex domain, `www`, and a wildcard. The script waits for the staging certificate to become Ready.

Use a real domain that is hosted in Namecheap, and set `NAMECHEAP_CLIENT_IP` to the public IPv4 address whitelisted in Namecheap. The webhook reads the credential Secret from the same namespace as the `Certificate`.

```bash
export DOMAIN='your-domain.example'
export ACME_EMAIL='you@example.com'
export NAMECHEAP_API_KEY='replace-with-namecheap-api-key'
export NAMECHEAP_API_USER='replace-with-namecheap-api-user'
export NAMECHEAP_CLIENT_IP='203.0.113.10'
export NAMESPACE='tls-demo'

./examples/quick_start.sh
```

The exact runnable script is [`examples/quick_start.sh`](examples/quick_start.sh). It uses the staging directory first:

```text
https://acme-staging-v02.api.letsencrypt.org/directory
```

A staging certificate proves that the ACME flow worked, but it is **not trusted by normal browsers**. “Successfully issued” and “trusted by ordinary clients” are different checks. A staging root can be installed in a test-only trust store, but never add it to a normal workstation or production trust store. Use Kubernetes status, the generated Secret, DNS TXT propagation, and—if needed—a test-only staging trust store to validate the integration. Do not use a staging certificate as production traffic's final certificate.

#### Complete setup

The complete script installs a pinned cert-manager chart, clones the pinned Namecheap webhook source tag, installs the webhook chart, creates the Namecheap credential Secret, issues a staging SAN certificate, and only then allows an explicit production promotion.

```bash
export DOMAIN='your-domain.example'
export ACME_EMAIL='you@example.com'
export NAMECHEAP_API_KEY='replace-with-namecheap-api-key'
export NAMECHEAP_API_USER='replace-with-namecheap-api-user'
export NAMECHEAP_CLIENT_IP='203.0.113.10'
export NAMESPACE='tls-demo'

# Default is staging-only. Set this only after staging is Ready and reviewed.
export PROMOTE_TO_PRODUCTION='false'

./examples/complete_setup.sh
```

The full script is [`examples/complete_setup.sh`](examples/complete_setup.sh). It uses these production values only when `PROMOTE_TO_PRODUCTION=true`:

- Production ACME directory: `https://acme-v02.api.letsencrypt.org/directory`
- A separate production `ClusterIssuer`: `letsencrypt-prod-namecheap`
- A separate production ACME account key Secret: `letsencrypt-prod-namecheap-account-key`
- A separate production certificate Secret: `${DOMAIN//./-}-production-tls`

The focused manifests are also available:

- [`examples/clusterissuer-staging.yaml`](examples/clusterissuer-staging.yaml) — staging `ClusterIssuer` with DNS-01 webhook configuration.
- [`examples/clusterissuer-production.yaml`](examples/clusterissuer-production.yaml) — production `ClusterIssuer`; only the ACME directory and account-key name differ.
- [`examples/certificate-sans.yaml`](examples/certificate-sans.yaml) — SAN certificate request with apex, `www`, and wildcard names.
- [`examples/namecheap-credentials.example.yaml`](examples/namecheap-credentials.example.yaml) — placeholder Secret shape; never commit real credentials.
- [`examples/verify.sh`](examples/verify.sh) — inspects issuer, certificate, order, challenge, Secret, and certificate SANs.

### How the Kubernetes flow works

1. You apply a `Certificate` with `dnsNames` and an `issuerRef` pointing to a `ClusterIssuer`.
2. cert-manager generates a private key and a `CertificateRequest`.
3. The ACME issuer creates an ACME `Order`. The order contains one or more authorizations for the requested names.
4. cert-manager creates a `Challenge` for each authorization that needs validation. You normally do not create `Order` or `Challenge` resources yourself.
5. The DNS-01 webhook receives the challenge. It calls Namecheap, adding a TXT record such as `_acme-challenge.your-domain.example` with the ACME key value.
6. cert-manager performs a self-check against DNS. It waits until the authoritative DNS servers return the expected TXT record.
7. Let's Encrypt performs its own DNS lookup. If every SAN authorization succeeds, it signs the certificate.
8. cert-manager stores the certificate chain in `tls.crt` and the private key in `tls.key` in the Secret named by `spec.secretName`.
9. Your Ingress, Gateway, load balancer, or application consumes that Secret. cert-manager watches the certificate and repeats the flow before expiry.

### ACME, Let's Encrypt, cert-manager, and Certbot

- **ACME** is the protocol. It defines accounts, orders, authorizations, challenges, certificate finalization, renewal information, and revocation.
- **Let's Encrypt** is one ACME Certificate Authority. It has separate staging and production environments.
- **cert-manager** is a Kubernetes controller and ACME client. It reconciles Kubernetes resources and stores output in Kubernetes Secrets.
- **Certbot** is another ACME client, normally run on a manually administered web server. It can edit NGINX or Apache configuration and schedule renewal on that server. You normally do not run Certbot for the same certificate that cert-manager manages; choose one owner for issuance and renewal.

The client/server relationship is worth remembering: ACME is the language, Let's Encrypt is the certificate office, and cert-manager or Certbot is the client speaking that language.

### HTTP-01 versus DNS-01

- **HTTP-01:** the client serves a token at `http://<name>/.well-known/acme-challenge/<token>`. It requires public port 80 and cannot issue wildcard certificates. In Kubernetes, cert-manager creates temporary solver resources and routes the request to an `acmesolver` Pod.
- **DNS-01:** the client publishes a TXT record at `_acme-challenge.<name>`. It supports wildcard certificates and does not require the application to be publicly reachable, but it requires an automatable DNS API. It also gives the solver powerful DNS credentials, so credential scope and isolation matter.

For the Namecheap scenario, DNS-01 is the natural choice because it supports `*.your-domain.example` and the webhook can update Namecheap DNS. The CA validates control of DNS, not that your application is running.

### What `ClusterIssuer` means

An `Issuer` is namespaced. A certificate in another namespace cannot directly use it. A `ClusterIssuer` is cluster-scoped and can be referenced by certificates in multiple namespaces:

```yaml
issuerRef:
  name: letsencrypt-prod
  kind: ClusterIssuer
  group: cert-manager.io
```

The ACME account key named by `spec.acme.privateKeySecretRef` is managed by cert-manager for the issuer. Keep the staging and production account-key names separate. The Namecheap credential references in this example are resolved by the webhook in the `Certificate`'s namespace, so place `namecheap-credentials` alongside the certificate. Do not assume a `ClusterIssuer` makes arbitrary Secrets cross-namespace.

### Understanding the Namecheap webhook

cert-manager's built-in ACME issuer supports standard HTTP-01 and several DNS-01 providers. A webhook is an external DNS solver that implements cert-manager's webhook contract. Its `groupName` identifies the webhook implementation and its `solverName` selects the solver inside that webhook:

```yaml
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
          clientIP: 203.0.113.10
```

The referenced implementation reads Namecheap DNS records, adds the ACME TXT record, calls Namecheap's `setHosts` operation, and later removes only the matching challenge record. Namecheap's `setHosts` behavior is important: records omitted from the request can be deleted, so a read-modify-write implementation must preserve all existing records. Concurrent DNS management is a production risk.

The archived webhook source uses a Namecheap API key, API username, and a `clientIP`. Namecheap requires API access and an IPv4 address on its whitelist. In a real deployment, route webhook egress through a stable NAT IPv4 and grant the API key only the permissions needed for the domain. Pin the webhook image by immutable digest, inspect the source, and maintain your own fork or choose a supported DNS provider before treating this as a production dependency.

### What production changes

The production `ClusterIssuer` is not a different Kubernetes kind. It is the same ACME configuration with the production directory URL and a different account key Secret. The production CA returns a publicly trusted chain; the staging CA returns a test chain that ordinary clients reject.

A production cutover should be deliberate:

1. Install or verify cert-manager and the webhook.
2. Create the Namecheap API credential Secret in the certificate namespace.
3. Apply the staging `ClusterIssuer`.
4. Request a staging SAN certificate.
5. Confirm `Certificate`, `Order`, and `Challenge` reach successful states. Confirm the `_acme-challenge` record appears and disappears correctly. Confirm `tls.crt` contains the requested SANs.
6. Review the webhook logs and the Namecheap record set. A staging certificate will not be browser-trusted unless you intentionally configure a test-only trust store.
7. Apply the production `ClusterIssuer` and request a production certificate with a new target Secret. Do not overwrite the staging Secret until the production Secret is Ready.
8. Point the Ingress or Gateway at the production Secret and verify from a normal client.
9. Leave renewal enabled and monitor `Certificate.status.renewalTime`, Ready conditions, Orders, Challenges, and webhook errors.

Let's Encrypt production has rate limits. Repeatedly deleting ACME account-key Secrets, recreating certificates while debugging, or changing the same SAN set can consume production capacity. The staging environment has separate accounts and a much larger test budget, so always debug the webhook and DNS propagation there first.

### Renewal and SAN behavior

A SAN (Subject Alternative Name) certificate contains multiple DNS names in one certificate. Every name must be validated. A certificate containing `your-domain.example`, `www.your-domain.example`, and `*.your-domain.example` can therefore create multiple authorizations and DNS challenges.

cert-manager calculates a renewal time from the certificate's actual lifetime. By default it attempts renewal around two-thirds through the lifetime; an explicit `renewBefore` or `renewBeforePercentage` can adjust the window. Let's Encrypt certificates are commonly 90 days, so renewing about 30 days before expiry is normal. Use Go duration syntax such as `2160h` and `360h`, not `90d` or `15d`.

Renewal produces a new certificate and, when private-key rotation is enabled, a new private key. Your workload must notice Secret updates. Some Ingress controllers reload automatically; an application that reads files only at startup may need a restart or a Secret reload mechanism.

### Troubleshooting checklist

```bash
kubectl get clusterissuer -o wide
kubectl describe clusterissuer letsencrypt-staging-namecheap
kubectl get certificate,certificaterequest,order,challenge -n tls-demo
kubectl describe challenge -n tls-demo
kubectl logs -n cert-manager deploy/namecheap-webhook-cert-manager-webhook-namecheap
kubectl get secret -n tls-demo namecheap-credentials
```

Interpret failures by layer:

- `ClusterIssuer` not Ready: ACME endpoint, account registration, or webhook configuration problem.
- `Challenge` stuck before presentation: solver selection, webhook APIService, RBAC, or Secret namespace problem.
- Challenge presented but self-check fails: DNS zone discovery, Namecheap API update, stale authoritative nameservers, or DNS propagation.
- Self-check passes but CA rejects it: the public DNS view differs from the cluster's view, the wrong TXT value is present, or the record was removed too early.
- Certificate Ready but the browser is not trusted: you are still serving the staging certificate, the Ingress references the wrong Secret, or the server is not presenting the full chain.

Use `kubectl describe` first. cert-manager places useful reasons and events on the `ClusterIssuer`, `Certificate`, `Order`, and `Challenge` resources.

## Research

### Reference URLs

- https://cert-manager.io/docs/configuration/acme/ — cert-manager's ACME issuer model, solver configuration, account key behavior, and staging/production examples.
- https://cert-manager.io/docs/concepts/acme-orders-challenges/ — the Kubernetes `Order` and `Challenge` resources and their lifecycle, scheduling, presentation, self-check, and cleanup behavior.
- https://cert-manager.io/docs/configuration/acme/dns01/webhook/ — how external DNS-01 webhooks are identified with `groupName`, `solverName`, and provider-specific configuration.
- https://letsencrypt.org/docs/staging-environment/ — the staging directory URL, separate staging accounts, staging rate limits, and the fact that staging roots are not in normal trust stores.
- https://letsencrypt.org/docs/challenge-types/ — the ACME HTTP-01 and DNS-01 validation mechanisms, wildcard support, propagation concerns, and credential risks.
- https://letsencrypt.org/docs/rate-limits/ — current production rate limits, renewal exemptions, authorization-failure limits, and guidance to use staging while troubleshooting.
- https://certbot.eff.org/pages/about — what Certbot is, where it fits, and how it differs from a Kubernetes-native controller.
- https://github.com/Extrality/cert-manager-webhook-namecheap — the Namecheap webhook implementation and its archived/unsupported status; use it as a reference to audit, not as an implicit production recommendation.

## Next steps

For deeper understanding, read the cert-manager `Certificate` and `Order` status fields while issuing a staging certificate, then trace the DNS TXT record from the authoritative nameserver to the ACME server's validation. For production, choose a supported DNS provider or maintain a reviewed, pinned Namecheap webhook with stable egress, scoped credentials, monitoring, backups, and a tested renewal path.
