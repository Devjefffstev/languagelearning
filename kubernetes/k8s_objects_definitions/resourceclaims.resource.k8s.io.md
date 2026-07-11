# Kind: ResourceClaim
### Version: resource.k8s.io/v1

```yaml
KIND:     ResourceClaim
VERSION:  resource.k8s.io/v1

DESCRIPTION:
     ResourceClaim describes a request for access to resources in the cluster,
     for use by workloads. For example, if a workload needs an accelerator
     device with specific properties, this is how that request is expressed. The
     status stanza tracks whether this claim has been satisfied and what
     specific resources have been allocated.

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
      devices	<Object>
         config	<[]Object>
            opaque	<Object>
               driver	<string>
               parameters	<map[string]>
            requests	<[]string>
         constraints	<[]Object>
            distinctAttribute	<string>
            matchAttribute	<string>
            requests	<[]string>
         requests	<[]Object>
            exactly	<Object>
               adminAccess	<boolean>
               allocationMode	<string>
               capacity	<Object>
                  requests	<map[string]string>
               count	<integer>
               deviceClassName	<string>
               selectors	<[]Object>
                  cel	<Object>
                     expression	<string>
               tolerations	<[]Object>
                  effect	<string>
                  key	<string>
                  operator	<string>
                  tolerationSeconds	<integer>
                  value	<string>
            firstAvailable	<[]Object>
               allocationMode	<string>
               capacity	<Object>
                  requests	<map[string]string>
               count	<integer>
               deviceClassName	<string>
               name	<string>
               selectors	<[]Object>
                  cel	<Object>
                     expression	<string>
               tolerations	<[]Object>
                  effect	<string>
                  key	<string>
                  operator	<string>
                  tolerationSeconds	<integer>
                  value	<string>
            name	<string>
   status	<Object>
      allocation	<Object>
         allocationTimestamp	<string>
         devices	<Object>
            config	<[]Object>
               opaque	<Object>
                  driver	<string>
                  parameters	<map[string]>
               requests	<[]string>
               source	<string>
            results	<[]Object>
               adminAccess	<boolean>
               bindingConditions	<[]string>
               bindingFailureConditions	<[]string>
               consumedCapacity	<map[string]string>
               device	<string>
               driver	<string>
               pool	<string>
               request	<string>
               shareID	<string>
               tolerations	<[]Object>
                  effect	<string>
                  key	<string>
                  operator	<string>
                  tolerationSeconds	<integer>
                  value	<string>
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
      devices	<[]Object>
         conditions	<[]Object>
            lastTransitionTime	<string>
            message	<string>
            observedGeneration	<integer>
            reason	<string>
            status	<string>
            type	<string>
         data	<map[string]>
         device	<string>
         driver	<string>
         networkData	<Object>
            hardwareAddress	<string>
            interfaceName	<string>
            ips	<[]string>
         pool	<string>
         shareID	<string>
      reservedFor	<[]Object>
         apiGroup	<string>
         name	<string>
         resource	<string>
         uid	<string>
```
