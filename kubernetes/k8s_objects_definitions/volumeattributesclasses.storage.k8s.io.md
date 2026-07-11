# Kind: VolumeAttributesClass
### Version: storage.k8s.io/v1

```yaml
KIND:     VolumeAttributesClass
VERSION:  storage.k8s.io/v1

DESCRIPTION:
     VolumeAttributesClass represents a specification of mutable volume
     attributes defined by the CSI driver. The class can be specified during
     dynamic provisioning of PersistentVolumeClaims, and changed in the
     PersistentVolumeClaim spec after provisioning.

FIELDS:
   apiVersion	<string>
   driverName	<string>
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
   parameters	<map[string]string>
```
