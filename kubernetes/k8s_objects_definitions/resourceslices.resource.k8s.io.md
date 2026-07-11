# Kind: ResourceSlice
### Version: resource.k8s.io/v1

```yaml
KIND:     ResourceSlice
VERSION:  resource.k8s.io/v1

DESCRIPTION:
     ResourceSlice represents one or more resources in a pool of similar
     resources, managed by a common driver. A pool may span more than one
     ResourceSlice, and exactly how many ResourceSlices comprise a pool is
     determined by the driver.

     At the moment, the only supported resources are devices with attributes and
     capacities. Each device in a given pool, regardless of how many
     ResourceSlices, must have a unique name. The ResourceSlice in which a
     device gets published may change over time. The unique identifier for a
     device is the tuple <driver name>, <pool name>, <device name>.

     Whenever a driver needs to update a pool, it increments the
     pool.Spec.Pool.Generation number and updates all ResourceSlices with that
     new number and new resource definitions. A consumer must only use
     ResourceSlices with the highest generation number and ignore all others.

     When allocating all resources in a pool matching certain criteria or when
     looking for the best solution among several different alternatives, a
     consumer should check the number of ResourceSlices in a pool (included in
     each ResourceSlice) to determine whether its view of a pool is complete and
     if not, should wait until the driver has completed updating the pool.

     For resources that are not local to a node, the node name is not set.
     Instead, the driver may use a node selector to specify where the devices
     are available.

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
      allNodes	<boolean>
      devices	<[]Object>
         allNodes	<boolean>
         allowMultipleAllocations	<boolean>
         attributes	<map[string]Object>
            bool	<boolean>
            int	<integer>
            string	<string>
            version	<string>
         bindingConditions	<[]string>
         bindingFailureConditions	<[]string>
         bindsToNode	<boolean>
         capacity	<map[string]Object>
            requestPolicy	<Object>
               default	<string>
               validRange	<Object>
                  max	<string>
                  min	<string>
                  step	<string>
               validValues	<[]string>
            value	<string>
         consumesCounters	<[]Object>
            counterSet	<string>
            counters	<map[string]Object>
               value	<string>
         name	<string>
         nodeName	<string>
         nodeSelector	<Object>
            nodeSelectorTerms	<[]Object>
               matchExpressions	<[]Object>
                  key	<string>
                  operator	<string>
                  values	<[]string>
               matchFields	<[]Object>
                  key	<string>
                  operator	<string>
                  values	<[]string>
         taints	<[]Object>
            effect	<string>
            key	<string>
            timeAdded	<string>
            value	<string>
      driver	<string>
      nodeName	<string>
      nodeSelector	<Object>
         nodeSelectorTerms	<[]Object>
            matchExpressions	<[]Object>
               key	<string>
               operator	<string>
               values	<[]string>
            matchFields	<[]Object>
               key	<string>
               operator	<string>
               values	<[]string>
      perDeviceNodeSelection	<boolean>
      pool	<Object>
         generation	<integer>
         name	<string>
         resourceSliceCount	<integer>
      sharedCounters	<[]Object>
         counters	<map[string]Object>
            value	<string>
         name	<string>
```
