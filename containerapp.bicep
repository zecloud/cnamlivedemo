@description('Name of the existing resource group')
param resourceGroupName string = 'cnamlivedemo'

@description('Location for the Container App')
param location string = resourceGroup().location

@description('Name of the Container App Environment (existing)')
param containerAppEnvName string = 'cnamenviron'

@description('Name for the Container App to create')
param containerAppName string = 'cnam-containerapp'

@description('Container image to deploy')
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

@description('Container port')
param containerPort int = 80

@description('Service Bus Namespace name for KEDA trigger')
param serviceBusNamespace string = 'cnamlivedemo'

@description('Service Bus Queue name for KEDA trigger')
param serviceBusQueue string = 'cnammessage'

@description('Minimum number of replicas for scale')
param minReplicas int = 0

@description('Maximum number of replicas for scale')
param maxReplicas int = 1

@description('Service Bus connection string secret name in container app secrets')
param serviceBusConnectionSecretName string = 'serviceBusConnection'

// Get the existing Container Apps environment
resource containerEnv 'Microsoft.Web/kubeEnvironments@2022-03-01' existing = {
  name: containerAppEnvName
}

// Create the Container App
resource containerApp 'Microsoft.Web/containerApps@2023-08-01-preview' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: containerPort
        transport: 'Auto'
      }
      registries: []
    }
    template: {
      containers: [
        {
          name: 'app'
          image: containerImage
          resources: {
            cpu: 0.25
            memory: '0.5Gi'
          }
          probes: []
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
        rules: [
          {
            name: 'keda-servicebus-trigger'
            custom: {
              type: 'azure-servicebus'
              metadata: {
                namespace: serviceBusNamespace
                queueName: serviceBusQueue
                messageCount: '1'
              }
              auth: [
                {
                  name: 'servicebus-connection'
                  secretRef: serviceBusConnectionSecretName
                }
              ]
            }
          }
        ]
      }
    }
    dapr: null
  }
}

// Expose the FQDN as an output
output containerAppFqdn string = containerApp.properties.configuration.ingress.fqdn
