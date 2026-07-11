# Kind: Event
### Version: v1

```yaml
KIND:     Event
VERSION:  v1

DESCRIPTION:
     Event is a report of an event somewhere in the cluster. Events have a
     limited retention time and triggers and messages may evolve with time.
     Event consumers should not rely on the timing of an event with a given
     Reason reflecting a consistent underlying trigger, or the continued
     existence of events with that Reason. Events should be treated as
     informative, best-effort, supplemental data.

FIELDS:
   action	<string>
   apiVersion	<string>
   count	<integer>
   eventTime	<string>
   firstTimestamp	<string>
   involvedObject	<Object>
      apiVersion	<string>
      fieldPath	<string>
      kind	<string>
      name	<string>
      namespace	<string>
      resourceVersion	<string>
      uid	<string>
   kind	<string>
   lastTimestamp	<string>
   message	<string>
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
   reason	<string>
   related	<Object>
      apiVersion	<string>
      fieldPath	<string>
      kind	<string>
      name	<string>
      namespace	<string>
      resourceVersion	<string>
      uid	<string>
   reportingComponent	<string>
   reportingInstance	<string>
   series	<Object>
      count	<integer>
      lastObservedTime	<string>
   source	<Object>
      component	<string>
      host	<string>
   type	<string>
```
