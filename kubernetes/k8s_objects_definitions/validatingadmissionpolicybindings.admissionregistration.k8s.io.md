# Kind: ValidatingAdmissionPolicyBinding
### Version: admissionregistration.k8s.io/v1

```yaml
KIND:     ValidatingAdmissionPolicyBinding
VERSION:  admissionregistration.k8s.io/v1

DESCRIPTION:
     ValidatingAdmissionPolicyBinding binds the ValidatingAdmissionPolicy with
     paramerized resources. ValidatingAdmissionPolicyBinding and parameter CRDs
     together define how cluster administrators configure policies for clusters.

     For a given admission request, each binding will cause its policy to be
     evaluated N times, where N is 1 for policies/bindings that don't use
     params, otherwise N is the number of parameters selected by the binding.

     The CEL expressions of a policy must have a computed CEL cost below the
     maximum CEL budget. Each evaluation of the policy is given an independent
     CEL cost budget. Adding/removing policies, bindings, or params can not
     affect whether a given (policy, binding, param) combination is within its
     own CEL budget.

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
      matchResources	<Object>
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
      paramRef	<Object>
         name	<string>
         namespace	<string>
         parameterNotFoundAction	<string>
         selector	<Object>
            matchExpressions	<[]Object>
               key	<string>
               operator	<string>
               values	<[]string>
            matchLabels	<map[string]string>
      policyName	<string>
      validationActions	<[]string>
```
