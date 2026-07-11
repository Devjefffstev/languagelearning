# Kind: IPAddress
### Version: networking.k8s.io/v1

```yaml
KIND:     IPAddress
VERSION:  networking.k8s.io/v1

DESCRIPTION:
     IPAddress represents a single IP of a single IP Family. The object is
     designed to be used by APIs that operate on IP addresses. The object is
     used by the Service core API for allocation of IP addresses. An IP address
     can be represented in different formats, to guarantee the uniqueness of the
     IP, the name of the object is the IP address in canonical format, four
     decimal digits separated by dots suppressing leading zeros for IPv4 and the
     representation defined by RFC 5952 for IPv6. Valid: 192.168.1.5 or
     2001:db8::1 or 2001:db8:aaaa:bbbb:cccc:dddd:eeee:1 Invalid: 10.01.2.3 or
     2001:db8:0:0:0::1

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
      parentRef	<Object>
         group	<string>
         name	<string>
         namespace	<string>
         resource	<string>
```
