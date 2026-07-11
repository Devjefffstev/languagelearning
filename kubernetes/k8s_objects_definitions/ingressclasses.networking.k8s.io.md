# Kind: IngressClass
### Version: networking.k8s.io/v1

```yaml
KIND:     IngressClass
VERSION:  networking.k8s.io/v1

DESCRIPTION:
     IngressClass represents the class of the Ingress, referenced by the Ingress
     Spec. The `ingressclass.kubernetes.io/is-default-class` annotation can be
     used to indicate that an IngressClass should be considered default. When a
     single IngressClass resource has this annotation set to true, new Ingress
     resources without a class specified will be assigned this default class.

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
      controller	<string>
      parameters	<Object>
         apiGroup	<string>
         kind	<string>
         name	<string>
         namespace	<string>
         scope	<string>
```
