# Kind: CSIStorageCapacity
### Version: storage.k8s.io/v1

```yaml
KIND:     CSIStorageCapacity
VERSION:  storage.k8s.io/v1

DESCRIPTION:
     CSIStorageCapacity stores the result of one CSI GetCapacity call. For a
     given StorageClass, this describes the available capacity in a particular
     topology segment. This can be used when considering where to instantiate
     new PersistentVolumes.

     For example this can express things like: - StorageClass "standard" has
     "1234 GiB" available in "topology.kubernetes.io/zone=us-east1" -
     StorageClass "localssd" has "10 GiB" available in
     "kubernetes.io/hostname=knode-abc123"

     The following three cases all imply that no capacity is available for a
     certain combination: - no object exists with suitable topology and storage
     class name - such an object exists, but the capacity is unset - such an
     object exists, but the capacity is zero

     The producer of these objects can decide which approach is more suitable.

     They are consumed by the kube-scheduler when a CSI driver opts into
     capacity-aware scheduling with CSIDriverSpec.StorageCapacity. The scheduler
     compares the MaximumVolumeSize against the requested size of pending
     volumes to filter out unsuitable nodes. If MaximumVolumeSize is unset, it
     falls back to a comparison against the less precise Capacity. If that is
     also unset, the scheduler assumes that capacity is insufficient and tries
     some other node.

FIELDS:
   apiVersion	<string>
   capacity	<string>
   kind	<string>
   maximumVolumeSize	<string>
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
   nodeTopology	<Object>
      matchExpressions	<[]Object>
         key	<string>
         operator	<string>
         values	<[]string>
      matchLabels	<map[string]string>
   storageClassName	<string>
```
