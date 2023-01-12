
### Install NFS Provisioners:

```
helm install nfs-provisioner-mle nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=nas.lely.dtml \
    --set nfs.path=/storage/nfsshare/data/MachineLearningEngineering \
    --set storageClass.name=nfsshare-mle \
    --set storageClass.provisionerName=k8s-sigs.io/nfs-provisioner-mle
```

### Install Nginx Ingress:

```
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --set controller.kind=Deployment \
  --set controller.service.type=NodePort \
  --set controller.nodeSelector."kubernetes\.io/hostname"=n3 \
  --set controller.hostPort.enabled=true \
  --set controller.metrics.enabled=true \
  --namespace kube-system
```


### Install Cert Manager:

```
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.8.0 \
  --set installCRDs=true \
  --set ingressShim.defaultIssuerName=letsencrypt-prod \
  --set ingressShim.defaultIssuerKind=ClusterIssuer \
  --set ingressShim.defaultIssuerGroup=cert-manager.io
```

### Install Cluster Issuer-prod:

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: <email>
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - dns01:
        azureDNS:
          clientID: <clientID>
          clientSecretSecretRef:
            name: service-principal-azuredns
            key: client-secret
          subscriptionID: <subscriptionID>
          tenantID: <tenantID>
          resourceGroupName: <resourceGroupName>
          hostedZoneName: <hostedZoneName>
          environment: AzurePublicCloud
```

### Install Cluster Issuer-staging:

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: <email>
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - dns01:
        azureDNS:
          clientID: <clientID>
          clientSecretSecretRef:
            name: service-principal-azuredns
            key: client-secret
          subscriptionID: <subscriptionID>
          tenantID: <tenantID>
          resourceGroupName: <resourceGroupName>
          hostedZoneName: <hostedZoneName>
          environment: AzurePublicCloud
```

### Change NodePort range in k3s:

```
k3s server --kube-apiserver-arg --service-node-port-range=20618-20828
```