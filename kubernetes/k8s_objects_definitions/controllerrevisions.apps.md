# Kind: ControllerRevision
### Version: apps/v1

```yaml
KIND:     ControllerRevision
VERSION:  apps/v1

DESCRIPTION:
     ControllerRevision implements an immutable snapshot of state data. Clients
     are responsible for serializing and deserializing the objects that contain
     their internal state. Once a ControllerRevision has been successfully
     created, it can not be updated. The API Server will fail validation of all
     requests that attempt to mutate the Data field. ControllerRevisions may,
     however, be deleted. Note that, due to its use by both the DaemonSet and
     StatefulSet controllers for update and rollback, this object is beta.
     However, it may be subject to name and representation changes in future
     releases, and clients should not depend on its stability. It is primarily
     for internal use by controllers.

FIELDS:
   apiVersion	<string>
   data	<map[string]>
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
   revision	<integer>
```
