# Kind: Endpoints
### Version: v1

```yaml
KIND:     Endpoints
VERSION:  v1

DESCRIPTION:
     Endpoints is a collection of endpoints that implement the actual service.
     Example:

     Name: "mysvc", Subsets: [ { Addresses: [{"ip": "10.10.1.1"}, {"ip":
     "10.10.2.2"}], Ports: [{"name": "a", "port": 8675}, {"name": "b", "port":
     309}] }, { Addresses: [{"ip": "10.10.3.3"}], Ports: [{"name": "a", "port":
     93}, {"name": "b", "port": 76}] }, ]

     Endpoints is a legacy API and does not contain information about all
     Service features. Use discoveryv1.EndpointSlice for complete information
     about Service endpoints.

     Deprecated: This API is deprecated in v1.33+. Use
     discoveryv1.EndpointSlice.

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
   subsets	<[]Object>
      addresses	<[]Object>
         hostname	<string>
         ip	<string>
         nodeName	<string>
         targetRef	<Object>
            apiVersion	<string>
            fieldPath	<string>
            kind	<string>
            name	<string>
            namespace	<string>
            resourceVersion	<string>
            uid	<string>
      notReadyAddresses	<[]Object>
         hostname	<string>
         ip	<string>
         nodeName	<string>
         targetRef	<Object>
            apiVersion	<string>
            fieldPath	<string>
            kind	<string>
            name	<string>
            namespace	<string>
            resourceVersion	<string>
            uid	<string>
      ports	<[]Object>
         appProtocol	<string>
         name	<string>
         port	<integer>
         protocol	<string>
```
