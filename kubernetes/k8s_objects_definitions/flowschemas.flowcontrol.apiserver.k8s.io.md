# Kind: FlowSchema
### Version: flowcontrol.apiserver.k8s.io/v1

```yaml
KIND:     FlowSchema
VERSION:  flowcontrol.apiserver.k8s.io/v1

DESCRIPTION:
     FlowSchema defines the schema of a group of flows. Note that a flow is made
     up of a set of inbound API requests with similar attributes and is
     identified by a pair of strings: the name of the FlowSchema and a "flow
     distinguisher".

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
      distinguisherMethod	<Object>
         type	<string>
      matchingPrecedence	<integer>
      priorityLevelConfiguration	<Object>
         name	<string>
      rules	<[]Object>
         nonResourceRules	<[]Object>
            nonResourceURLs	<[]string>
            verbs	<[]string>
         resourceRules	<[]Object>
            apiGroups	<[]string>
            clusterScope	<boolean>
            namespaces	<[]string>
            resources	<[]string>
            verbs	<[]string>
         subjects	<[]Object>
            group	<Object>
               name	<string>
            kind	<string>
            serviceAccount	<Object>
               name	<string>
               namespace	<string>
            user	<Object>
               name	<string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         reason	<string>
         status	<string>
         type	<string>
```
