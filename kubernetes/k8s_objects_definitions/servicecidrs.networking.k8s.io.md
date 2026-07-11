# Kind: ServiceCIDR
### Version: networking.k8s.io/v1

```yaml
KIND:     ServiceCIDR
VERSION:  networking.k8s.io/v1

DESCRIPTION:
     ServiceCIDR defines a range of IP addresses using CIDR format (e.g.
     192.168.0.0/24 or 2001:db2::/64). This range is used to allocate ClusterIPs
     to Service objects.

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
      cidrs	<[]string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         observedGeneration	<integer>
         reason	<string>
         status	<string>
         type	<string>
```
