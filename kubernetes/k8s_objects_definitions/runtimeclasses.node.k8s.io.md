# Kind: RuntimeClass
### Version: node.k8s.io/v1

```yaml
KIND:     RuntimeClass
VERSION:  node.k8s.io/v1

DESCRIPTION:
     RuntimeClass defines a class of container runtime supported in the cluster.
     The RuntimeClass is used to determine which container runtime is used to
     run all containers in a pod. RuntimeClasses are manually defined by a user
     or cluster provisioner, and referenced in the PodSpec. The Kubelet is
     responsible for resolving the RuntimeClassName reference before running the
     pod. For more details, see
     https://kubernetes.io/docs/concepts/containers/runtime-class/

FIELDS:
   apiVersion	<string>
   handler	<string>
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
   overhead	<Object>
      podFixed	<map[string]string>
   scheduling	<Object>
      nodeSelector	<map[string]string>
      tolerations	<[]Object>
         effect	<string>
         key	<string>
         operator	<string>
         tolerationSeconds	<integer>
         value	<string>
```
