# Kind: Service
### Version: v1

```yaml
KIND:     Service
VERSION:  v1

DESCRIPTION:
     Service is a named abstraction of software service (for example, mysql)
     consisting of local port (for example 3306) that the proxy listens on, and
     the selector that determines which pods will answer requests sent through
     the proxy.

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
      allocateLoadBalancerNodePorts	<boolean>
      clusterIP	<string>
      clusterIPs	<[]string>
      externalIPs	<[]string>
      externalName	<string>
      externalTrafficPolicy	<string>
      healthCheckNodePort	<integer>
      internalTrafficPolicy	<string>
      ipFamilies	<[]string>
      ipFamilyPolicy	<string>
      loadBalancerClass	<string>
      loadBalancerIP	<string>
      loadBalancerSourceRanges	<[]string>
      ports	<[]Object>
         appProtocol	<string>
         name	<string>
         nodePort	<integer>
         port	<integer>
         protocol	<string>
         targetPort	<string>
      publishNotReadyAddresses	<boolean>
      selector	<map[string]string>
      sessionAffinity	<string>
      sessionAffinityConfig	<Object>
         clientIP	<Object>
            timeoutSeconds	<integer>
      trafficDistribution	<string>
      type	<string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         observedGeneration	<integer>
         reason	<string>
         status	<string>
         type	<string>
      loadBalancer	<Object>
         ingress	<[]Object>
            hostname	<string>
            ip	<string>
            ipMode	<string>
            ports	<[]Object>
               error	<string>
               port	<integer>
               protocol	<string>
```
