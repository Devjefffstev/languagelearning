# Kind: PriorityLevelConfiguration
### Version: flowcontrol.apiserver.k8s.io/v1

```yaml
KIND:     PriorityLevelConfiguration
VERSION:  flowcontrol.apiserver.k8s.io/v1

DESCRIPTION:
     PriorityLevelConfiguration represents the configuration of a priority
     level.

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
      exempt	<Object>
         lendablePercent	<integer>
         nominalConcurrencyShares	<integer>
      limited	<Object>
         borrowingLimitPercent	<integer>
         lendablePercent	<integer>
         limitResponse	<Object>
            queuing	<Object>
               handSize	<integer>
               queueLengthLimit	<integer>
               queues	<integer>
            type	<string>
         nominalConcurrencyShares	<integer>
      type	<string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         reason	<string>
         status	<string>
         type	<string>
```
