# AWS Services

## Compute

| Service | Use Case | Key Feature |
|---------|----------|-------------|
| **EC2** | Virtual servers | Full control, any workload |
| **Lambda** | Serverless functions | Pay per invocation, auto-scales to zero |
| **ECS/Fargate** | Container orchestration | Docker containers without managing servers |
| **EKS** | Kubernetes | Managed Kubernetes clusters |

### Lambda Example

```python
import json

def handler(event, context):
    name = event.get("name", "World")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Hello, {name}!"})
    }
```

## Storage

| Service | Type | Use Case |
|---------|------|----------|
| **S3** | Object storage | Files, backups, static websites |
| **EBS** | Block storage | EC2 disk volumes |
| **EFS** | File storage | Shared filesystem across instances |
| **Glacier** | Archive | Long-term, infrequent access |

### S3 Key Concepts

```bash
# AWS CLI
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./dist s3://my-bucket/ --delete
aws s3 ls s3://my-bucket/
```

- **Bucket** - Container for objects (globally unique name)
- **Storage classes** - Standard, IA (Infrequent Access), Glacier
- **Lifecycle rules** - Auto-transition objects between classes

## Database

| Service | Type | Best For |
|---------|------|----------|
| **RDS** | Relational | PostgreSQL, MySQL, managed |
| **DynamoDB** | Key-value/Document | High-scale, low-latency |
| **ElastiCache** | In-memory | Redis/Memcached caching |
| **Aurora** | Relational | High-performance MySQL/PostgreSQL |

## Networking

- **VPC** - Virtual private network for your resources
- **ALB** - Application Load Balancer for HTTP traffic
- **Route 53** - DNS and domain management
- **CloudFront** - CDN for global content delivery

## SageMaker

### Overview

Amazon SageMaker is a fully managed machine learning service for building, training, and deploying ML models at scale.

### Key Components

| Component | Purpose |
|-----------|---------|
| **Studio** | Web-based IDE for ML development |
| **Notebooks** | Managed Jupyter notebooks with pre-configured environments |
| **Training Jobs** | Scalable model training on managed infrastructure |
| **Endpoints** | Real-time model hosting and inference |
| **Pipelines** | CI/CD for ML workflows |
| **Feature Store** | Centralized repository for ML features |
| **Model Registry** | Version and manage trained models |
| **Ground Truth** | Data labeling service |

### Workflow

```
Data (S3) → Notebook/Processing → Training Job → Model → Endpoint
                                      ↓
                               Model Registry
                                      ↓
                               SageMaker Pipeline (CI/CD)
```

### Training Example

```python
import sagemaker
from sagemaker.estimator import Estimator

session = sagemaker.Session()
role = sagemaker.get_execution_role()

estimator = Estimator(
    image_uri="123456789.dkr.ecr.us-east-1.amazonaws.com/my-model:latest",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    output_path="s3://my-bucket/models/",
)

estimator.fit({"train": "s3://my-bucket/data/train/"})
```

### Deploying a Model

```python
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
)

result = predictor.predict(test_data)

# Clean up when done
predictor.delete_endpoint()
```

### Built-in Algorithms

| Algorithm | Type | Use Case |
|-----------|------|----------|
| **XGBoost** | Supervised | Classification, regression |
| **BlazingText** | NLP | Text classification, Word2Vec |
| **Image Classification** | Vision | Image labeling |
| **DeepAR** | Time series | Forecasting |
| **K-Means** | Unsupervised | Clustering |

### Cost Tips

- Use **Spot Training** for up to 90% savings on training jobs
- Choose **Serverless Inference** for intermittent traffic
- Use **Auto Scaling** on endpoints to match demand
- Stop idle **Notebook Instances** when not in use

## Common Architecture

```
User → CloudFront (CDN) → ALB → ECS/EC2 → RDS
                                    ↓
                              ElastiCache (Redis)
                                    ↓
                               S3 (files)
```

## Cost Optimization Tips

- Use **Spot Instances** for fault-tolerant workloads (up to 90% savings)
- Enable **S3 Intelligent Tiering** for unpredictable access patterns
- Set up **Budget Alerts** in AWS Billing
- Use **Reserved Instances** for steady-state workloads (1-3 year commitment)
- Review **Trusted Advisor** recommendations monthly
