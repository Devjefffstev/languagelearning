# Kind: Namespace
### Version: v1

```yaml
KIND:     Namespace
VERSION:  v1

DESCRIPTION:
     Namespace provides a scope for Names. Use of multiple namespaces is
     optional.

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
      finalizers	<[]string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         reason	<string>
         status	<string>
         type	<string>
      phase	<string>
```
