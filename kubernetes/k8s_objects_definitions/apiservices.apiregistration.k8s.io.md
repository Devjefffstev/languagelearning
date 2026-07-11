# Kind: APIService
### Version: apiregistration.k8s.io/v1

```yaml
KIND:     APIService
VERSION:  apiregistration.k8s.io/v1

DESCRIPTION:
     APIService represents a server for a particular GroupVersion. Name must be
     "version.group".

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
      caBundle	<string>
      group	<string>
      groupPriorityMinimum	<integer>
      insecureSkipTLSVerify	<boolean>
      service	<Object>
         name	<string>
         namespace	<string>
         port	<integer>
      version	<string>
      versionPriority	<integer>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         reason	<string>
         status	<string>
         type	<string>
```
