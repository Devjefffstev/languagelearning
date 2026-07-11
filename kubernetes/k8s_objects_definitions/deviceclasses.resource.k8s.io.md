# Kind: DeviceClass
### Version: resource.k8s.io/v1

```yaml
KIND:     DeviceClass
VERSION:  resource.k8s.io/v1

DESCRIPTION:
     DeviceClass is a vendor- or admin-provided resource that contains device
     configuration and selectors. It can be referenced in the device requests of
     a claim to apply these presets. Cluster scoped.

     This is an alpha type and requires enabling the DynamicResourceAllocation
     feature gate.

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
      config	<[]Object>
         opaque	<Object>
            driver	<string>
            parameters	<map[string]>
      extendedResourceName	<string>
      selectors	<[]Object>
         cel	<Object>
            expression	<string>
```
