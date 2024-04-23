#!/bin/bash

# Define directories
DEPLOYMENTS_DIR="deployments"
SERVICES_DIR="services"
SECRETS_DIR="secrets"

kubectl delete deployment app-deployment
echo "Sleep 2 seconds"
sleep 2
## Delete old app image
minikube image rm book_web_service-app
# Load new app image
minikube image load book_web_service-app
docker context use default
#minikube cache add book_web_service-app:latest
#minikube cache reload
#minikube cache list

# Apply deployment manifests
for file in $DEPLOYMENTS_DIR/*.yaml; do
    kubectl apply -f "$file"
done

# Apply service manifests
for file in $SERVICES_DIR/*.yaml; do
    kubectl apply -f "$file"
done

# Apply secret manifests
for file in $SECRETS_DIR/*.yaml; do
    kubectl apply -f "$file"
done