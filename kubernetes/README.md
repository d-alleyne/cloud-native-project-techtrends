## Kubernetes Declarative Manifests 

1) Create a sandbox namespace manifest file. 

    ```kubectl create namespace sandbox --dry-run=client -oyaml > kubernetes/namespace.yaml```
2) Create a deployment manifest file, then modify the resources and readiness and liveness probes.

   ``` kubectl.exe create deploy techtrends -nsandbox --image=nashblade/techtrends --dry-run=client --port=3111 -oyaml > kubernetes/deploy.yaml```
3) Create a service.yaml file which is clusterIP, and redirects incoming traffic from port 4111 to 3111 of the deployment

    ``` kubectl create service clusterip techtrends --tcp=4111:3111 -nsandbox --dry-run=client -oyaml > .kubernetes/service.yaml```