# Kind: CSINode
### Version: storage.k8s.io/v1

```yaml
KIND:     CSINode
VERSION:  storage.k8s.io/v1

DESCRIPTION:
     CSINode holds information about all CSI drivers installed on a node. CSI
     drivers do not need to create the CSINode object directly. As long as they
     use the node-driver-registrar sidecar container, the kubelet will
     automatically populate the CSINode object for the CSI driver as part of
     kubelet plugin registration. CSINode has the same name as a node. If the
     object is missing, it means either there are no CSI Drivers available on
     the node, or the Kubelet version is low enough that it doesn't create this
     object. CSINode has an OwnerReference that points to the corresponding node
     object.

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
      drivers	<[]Object>
         allocatable	<Object>
            count	<integer>
         name	<string>
         nodeID	<string>
         topologyKeys	<[]string>
```
