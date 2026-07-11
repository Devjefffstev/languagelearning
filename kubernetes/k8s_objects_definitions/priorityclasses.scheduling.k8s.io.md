# Kind: PriorityClass
### Version: scheduling.k8s.io/v1

```yaml
KIND:     PriorityClass
VERSION:  scheduling.k8s.io/v1

DESCRIPTION:
     PriorityClass defines mapping from a priority class name to the priority
     integer value. The value can be any valid integer.

FIELDS:
   apiVersion	<string>
   description	<string>
   globalDefault	<boolean>
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
   preemptionPolicy	<string>
   value	<integer>
```
