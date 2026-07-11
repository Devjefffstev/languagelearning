# Kind: LimitRange
### Version: v1

```yaml
KIND:     LimitRange
VERSION:  v1

DESCRIPTION:
     LimitRange sets resource usage limits for each kind of resource in a
     Namespace.

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
      limits	<[]Object>
         default	<map[string]string>
         defaultRequest	<map[string]string>
         max	<map[string]string>
         maxLimitRequestRatio	<map[string]string>
         min	<map[string]string>
         type	<string>
```
