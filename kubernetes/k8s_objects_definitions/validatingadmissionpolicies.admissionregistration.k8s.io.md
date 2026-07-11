# Kind: ValidatingAdmissionPolicy
### Version: admissionregistration.k8s.io/v1

```yaml
KIND:     ValidatingAdmissionPolicy
VERSION:  admissionregistration.k8s.io/v1

DESCRIPTION:
     ValidatingAdmissionPolicy describes the definition of an admission
     validation policy that accepts or rejects an object without changing it.

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
      auditAnnotations	<[]Object>
         key	<string>
         valueExpression	<string>
      failurePolicy	<string>
      matchConditions	<[]Object>
         expression	<string>
         name	<string>
      matchConstraints	<Object>
         excludeResourceRules	<[]Object>
            apiGroups	<[]string>
            apiVersions	<[]string>
            operations	<[]string>
            resourceNames	<[]string>
            resources	<[]string>
            scope	<string>
         matchPolicy	<string>
         namespaceSelector	<Object>
            matchExpressions	<[]Object>
               key	<string>
               operator	<string>
               values	<[]string>
            matchLabels	<map[string]string>
         objectSelector	<Object>
            matchExpressions	<[]Object>
               key	<string>
               operator	<string>
               values	<[]string>
            matchLabels	<map[string]string>
         resourceRules	<[]Object>
            apiGroups	<[]string>
            apiVersions	<[]string>
            operations	<[]string>
            resourceNames	<[]string>
            resources	<[]string>
            scope	<string>
      paramKind	<Object>
         apiVersion	<string>
         kind	<string>
      validations	<[]Object>
         expression	<string>
         message	<string>
         messageExpression	<string>
         reason	<string>
      variables	<[]Object>
         expression	<string>
         name	<string>
   status	<Object>
      conditions	<[]Object>
         lastTransitionTime	<string>
         message	<string>
         observedGeneration	<integer>
         reason	<string>
         status	<string>
         type	<string>
      observedGeneration	<integer>
      typeChecking	<Object>
         expressionWarnings	<[]Object>
            fieldRef	<string>
            warning	<string>
```
