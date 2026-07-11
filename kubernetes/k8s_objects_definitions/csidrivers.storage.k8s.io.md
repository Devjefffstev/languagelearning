# Kind: CSIDriver
### Version: storage.k8s.io/v1

```yaml
KIND:     CSIDriver
VERSION:  storage.k8s.io/v1

DESCRIPTION:
     CSIDriver captures information about a Container Storage Interface (CSI)
     volume driver deployed on the cluster. Kubernetes attach detach controller
     uses this object to determine whether attach is required. Kubelet uses this
     object to determine whether pod information needs to be passed on mount.
     CSIDriver objects are non-namespaced.

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
      attachRequired	<boolean>
      fsGroupPolicy	<string>
      nodeAllocatableUpdatePeriodSeconds	<integer>
      podInfoOnMount	<boolean>
      requiresRepublish	<boolean>
      seLinuxMount	<boolean>
      serviceAccountTokenInSecrets	<boolean>
      storageCapacity	<boolean>
      tokenRequests	<[]Object>
         audience	<string>
         expirationSeconds	<integer>
      volumeLifecycleModes	<[]string>
```
