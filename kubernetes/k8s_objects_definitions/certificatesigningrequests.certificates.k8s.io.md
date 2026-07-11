# Kind: CertificateSigningRequest
### Version: certificates.k8s.io/v1

```yaml
KIND:     CertificateSigningRequest
VERSION:  certificates.k8s.io/v1

DESCRIPTION:
     CertificateSigningRequest objects provide a mechanism to obtain x509
     certificates by submitting a certificate signing request, and having it
     asynchronously approved and issued.

     Kubelets use this API to obtain:
     1. client certificates to authenticate to kube-apiserver (with the
     "kubernetes.io/kube-apiserver-client-kubelet" signerName).
     2. serving certificates for TLS endpoints kube-apiserver can connect to
     securely (with the "kubernetes.io/kubelet-serving" signerName).

     This API can be used to request client certificates to authenticate to
     kube-apiserver (with the "kubernetes.io/kube-apiserver-client" signerName),
     or to obtain certificates from custom non-Kubernetes signers.

FIELDS:
   apiVersion	<string>
   kind	<string>
   metadata	<Object>
      annotations	<map[string]string>
      creationTimestamp	<string>
      deletionGracePeriodSeconds	<integer>
      deletionTimestamp	<string>
      finalizers	<[]string>
      generateName	<string>
      generation	<integer>
      labels	<map[string]string>
      managedFields	<[]Object>
         apiVersion	<string>
         fieldsType	<string>
         fieldsV1	<map[string]>
         manager	<string>
         operation	<string>
         subresource	<string>
         time	<string>
      name	<string>
      namespace	<string>
      ownerReferences	<[]Object>
         apiVersion	<string>
         blockOwnerDeletion	<boolean>
         controller	<boolean>
         kind	<string>
         name	<string>
         uid	<string>
      resourceVersion	<string>
      selfLink	<string>
      uid	<string>
   spec	<Object>
      expirationSeconds	<integer>
      extra	<map[string][]string>
      groups	<[]string>
      request	<string>
      signerName	<string>
      uid	<string>
      usages	<[]string>
      username	<string>
   status	<Object>
      certificate	<string>
      conditions	<[]Object>
         lastTransitionTime	<string>
         lastUpdateTime	<string>
         message	<string>
         reason	<string>
         status	<string>
         type	<string>
```
