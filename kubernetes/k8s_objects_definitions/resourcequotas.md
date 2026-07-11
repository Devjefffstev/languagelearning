# Kind: ResourceQuota
### Version: v1

```yaml
KIND:     ResourceQuota
VERSION:  v1

DESCRIPTION:
     ResourceQuota sets aggregate quota restrictions enforced per namespace

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
      hard	<map[string]string>
      scopeSelector	<Object>
         matchExpressions	<[]Object>
            operator	<string>
            scopeName	<string>
            values	<[]string>
      scopes	<[]string>
   status	<Object>
      hard	<map[string]string>
      used	<map[string]string>
```
