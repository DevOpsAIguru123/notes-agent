# Azure Basics

## Core Services (AWS Equivalent)

| Azure Service | Purpose | AWS Equivalent |
|---------------|---------|---------------|
| **Virtual Machines** | Compute instances | EC2 |
| **Azure Functions** | Serverless | Lambda |
| **App Service** | Managed web apps | Elastic Beanstalk |
| **AKS** | Managed Kubernetes | EKS |
| **Blob Storage** | Object storage | S3 |
| **Azure SQL** | Managed database | RDS |
| **Cosmos DB** | Multi-model NoSQL | DynamoDB |
| **Azure AD (Entra ID)** | Identity & access | IAM + Cognito |

## Resource Organization

```
Tenant (Azure AD)
  └── Management Group
       └── Subscription (billing boundary)
            └── Resource Group (logical container)
                 ├── Virtual Machine
                 ├── Storage Account
                 └── App Service
```

!!! tip "Resource Groups"
    Group resources by lifecycle. If they're deployed together and deleted together, they belong in the same resource group.

## Azure CLI

```bash
# Login
az login

# Create a resource group
az group create --name myapp-rg --location eastus

# Create an App Service
az webapp create \
  --resource-group myapp-rg \
  --name myapp-web \
  --runtime "PYTHON:3.12" \
  --sku B1

# Deploy from local
az webapp up --name myapp-web --runtime "PYTHON:3.12"

# List resources
az resource list --resource-group myapp-rg --output table
```

## Azure Functions

```python
import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "World")
    return func.HttpResponse(
        json.dumps({"message": f"Hello, {name}!"}),
        mimetype="application/json"
    )
```

## Blob Storage

```python
from azure.storage.blob import BlobServiceClient

connection_string = "DefaultEndpointsProtocol=https;..."
client = BlobServiceClient.from_connection_string(connection_string)

# Upload
blob = client.get_blob_client("mycontainer", "data.json")
with open("data.json", "rb") as f:
    blob.upload_blob(f, overwrite=True)

# Download
with open("downloaded.json", "wb") as f:
    f.write(blob.download_blob().readall())
```

## Key Differences from AWS

| Aspect | AWS | Azure |
|--------|-----|-------|
| Identity | IAM (per-account) | Azure AD (org-wide) |
| Billing unit | Account | Subscription |
| IaC tool | CloudFormation | ARM/Bicep templates |
| CLI | `aws` | `az` |
| Serverless | Lambda (zip/container) | Functions (project-based) |
| Strength | Broadest service catalog | Enterprise/hybrid integration |
