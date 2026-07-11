# Kind: EndpointSlice
### Version: discovery.k8s.io/v1

```yaml
KIND:     EndpointSlice
VERSION:  discovery.k8s.io/v1

DESCRIPTION:
     EndpointSlice represents a set of service endpoints. Most EndpointSlices
     are created by the EndpointSlice controller to represent the Pods selected
     by Service objects. For a given service there may be multiple EndpointSlice
     objects which must be joined to produce the full set of endpoints; you can
     find all of the slices for a given service by listing EndpointSlices in the
     service's namespace whose `kubernetes.io/service-name` label contains the
     service's name.

FIELDS:
   addressType	<string>
   apiVersion	<string>
   endpoints	<[]Object>
      addresses	<[]string>
      conditions	<Object>
         ready	<boolean>
         serving	<boolean>
         terminating	<boolean>
      deprecatedTopology	<map[string]string>
      hints	<Object>
         forNodes	<[]Object>
            name	<string>
         forZones	<[]Object>
            name	<string>
      hostname	<string>
      nodeName	<string>
      targetRef	<Object>
         apiVersion	<string>
         fieldPath	<string>
         kind	<string>
         name	<string>
         namespace	<string>
         resourceVersion	<string>
         uid	<string>
      zone	<string>
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
   ports	<[]Object>
      appProtocol	<string>
      name	<string>
      port	<integer>
      protocol	<string>
```
