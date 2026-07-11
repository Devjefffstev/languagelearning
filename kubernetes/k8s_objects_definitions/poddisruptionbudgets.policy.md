# Kind: PodDisruptionBudget
### Version: policy/v1

```yaml
KIND:     PodDisruptionBudget
VERSION:  policy/v1

DESCRIPTION:
     PodDisruptionBudget is an object to define the max disruption that can be
     caused to a collection of pods

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
      maxUnavailable	<string>
      minAvailable	<string>
      selector	<Object>
         matchExpressions	<[]Object>
            key	<string>
            operator	<string>
            values	<[]string>
         matchLabels	<map[string]string>
      unhealthyPodEvictionPolicy	<string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         observedGeneration	<integer>
         reason	<string>
         status	<string>
         type	<string>
      currentHealthy	<integer>
      desiredHealthy	<integer>
      disruptedPods	<map[string]string>
      disruptionsAllowed	<integer>
      expectedPods	<integer>
      observedGeneration	<integer>
```
