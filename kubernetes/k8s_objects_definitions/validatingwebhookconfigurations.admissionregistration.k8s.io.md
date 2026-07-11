# Kind: ValidatingWebhookConfiguration
### Version: admissionregistration.k8s.io/v1

```yaml
KIND:     ValidatingWebhookConfiguration
VERSION:  admissionregistration.k8s.io/v1

DESCRIPTION:
     ValidatingWebhookConfiguration describes the configuration of and admission
     webhook that accept or reject and object without changing it.

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
   webhooks	<[]Object>
      admissionReviewVersions	<[]string>
      clientConfig	<Object>
         caBundle	<string>
         service	<Object>
            name	<string>
            namespace	<string>
            path	<string>
            port	<integer>
         url	<string>
      failurePolicy	<string>
      matchConditions	<[]Object>
         expression	<string>
         name	<string>
      matchPolicy	<string>
      name	<string>
      namespaceSelector	<Object>
         matchExpressions	<[]Object>
            key	<string>
            operator	<string>
            values	<[]string>
         matchLabels	<map[string]string>
      objectSelector	<Object>
         matchExpressions	<[]Object>
            key	<string>
            operator	<string>
            values	<[]string>
         matchLabels	<map[string]string>
      rules	<[]Object>
         apiGroups	<[]string>
         apiVersions	<[]string>
         operations	<[]string>
         resources	<[]string>
         scope	<string>
      sideEffects	<string>
      timeoutSeconds	<integer>
```
