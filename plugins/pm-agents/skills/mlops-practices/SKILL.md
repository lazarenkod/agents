---
name: mlops-practices
description: MLOps best practices for managing ML/AI infrastructure projects including model lifecycle, deployment pipelines, monitoring, and governance. Use when planning ML infrastructure, model deployment, or AI/ML platform development.
---

# MLOps Practices

Comprehensive MLOps framework для управления ML/AI проектами от training до production.

## When to Use This Skill

- Planning ML infrastructure projects
- Model deployment и production systems
- ML platform development
- AI/ML technical project management
- LLM integration projects (OpenAI, Claude)
- ML model lifecycle management

## Core Concepts

### ML Project Lifecycle

```
Data Collection → Data Preparation → Model Training →
Model Evaluation → Model Deployment → Monitoring →
Retraining (loop back)
```

### MLOps Maturity Levels

**Level 0: Manual Process**
- Manual data analysis
- Model training в notebooks
- Manual deployment
- No automation

**Level 1: ML Pipeline Automation**
- Automated training pipeline
- Automated model validation
- Модель serving infrastructure
- Manual retraining trigger

**Level 2: CI/CD для ML**
- Automated training pipeline
- Automated model deployment
- Continuous training
- Automated monitoring & retraining
- Feature store integration
- Model registry

## Key Components

### 1. Data Management

**Data Collection:**
- Streaming data pipelines (Kafka, Kinesis)
- Batch data ingestion (Airflow, Prefect)
- Data quality validation
- Data versioning (DVC, lakeFS)

**Feature Engineering:**
- Feature stores (Feast, Tecton, SageMaker)
- Feature transformation pipelines
- Feature versioning
- Online/offline consistency

### 2. Model Training

**Training Infrastructure:**
- GPU clusters (AWS P4, Azure NCv4, GCP A100)
- Distributed training (Horovod, DeepSpeed)
- Experiment tracking (MLflow, Weights & Biases)
- Hyperparameter tuning (Optuna, Ray Tune)

**Training Pipeline:**
```python
# Example pipeline structure
train_pipeline = {
    'data_validation': validate_data(),
    'preprocessing': preprocess(),
    'training': train_model(),
    'evaluation': evaluate_model(),
    'model_validation': validate_model(),
    'model_registration': register_model()
}
```

### 3. Model Deployment

**Serving Options:**
- **Batch Inference**: Scheduled predictions (Airflow)
- **Real-time**: REST API (TensorFlow Serving, TorchServe)
- **Streaming**: Stream processing (Kafka, Flink)

**Deployment Strategies:**
- **Blue-Green**: Two environments, instant switch
- **Canary**: Gradual traffic shift (5%→25%→100%)
- **Shadow**: Parallel deployment без affecting users
- **A/B Testing**: Multiple models simultaneously

### 4. Model Monitoring

**Metrics to Track:**

**Performance Metrics:**
- Accuracy, precision, recall, F1
- Latency (p50, p95, p99)
- Throughput (requests/sec)

**Model Quality:**
- Prediction drift detection
- Feature drift (PSI, KL divergence)
- Data quality issues

**Business Metrics:**
- Revenue impact
- User engagement
- Conversion rates

**Infrastructure:**
- CPU/GPU utilization
- Memory usage
- Cost per prediction

### 5. LLM-Specific Practices

**Prompt Management:**
- Prompt versioning
- Prompt templates library
- A/B testing prompts
- Evaluation frameworks

**RAG Architecture:**
```
User Query →
Embedding →
Vector Search (Pinecone, Weaviate) →
Context Retrieval →
LLM (OpenAI, Claude) →
Response Generation →
Validation →
User
```

**LLM Monitoring:**
- Token usage tracking
- Cost per request
- Response latency
- Quality evaluation (BLEU, ROUGE)
- Hallucination detection

## MLOps Tech Stack

### Cloud Platforms

**AWS:**
- SageMaker (training, deployment)
- Lambda (inference)
- Step Functions (orchestration)
- S3 (data storage)

**Azure:**
- Azure ML (end-to-end platform)
- Functions (inference)
- Synapse (data processing)
- Blob Storage

**GCP:**
- Vertex AI (training, deployment)
- Cloud Functions (inference)
- Dataflow (processing)
- BigQuery (data warehouse)

### Tools Ecosystem

**Experiment Tracking:**
- MLflow, Weights & Biases, Neptune.ai

**Model Registry:**
- MLflow Model Registry, SageMaker Registry

**Feature Stores:**
- Feast, Tecton, SageMaker Feature Store

**Data Versioning:**
- DVC, lakeFS, Pachyderm

**Orchestration:**
- Airflow, Prefect, Kubeflow Pipelines

**Monitoring:**
- WhyLabs, Arize, Fiddler

## Project Planning Template

```markdown
# ML Project Plan - [Project Name]

## Problem Definition

**Business Objective**: [What problem solving]
**Success Metrics**: [How measure success]
**Baseline**: [Current performance]
**Target**: [Goal performance]

## Data Strategy

**Data Sources**:
- [Source 1]: [Volume, frequency]
- [Source 2]: [Volume, frequency]

**Data Quality Requirements**:
- [Requirement 1]
- [Requirement 2]

**Feature Engineering**:
- [Key features to develop]

## Model Strategy

**Model Type**: [Classification/Regression/LLM/etc.]
**Algorithms to Try**: [List 3-5 approaches]
**Evaluation Metrics**: [Primary and secondary]
**Success Criteria**: [Minimum acceptable performance]

## Infrastructure Requirements

**Training**:
- Compute: [GPU type, count]
- Storage: [TB needed]
- Estimated cost: $[X]/month

**Serving**:
- Latency requirement: <[X]ms p95
- Throughput: [N] requests/sec
- Availability: [X]%

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Data Exploration | 2 weeks | Data quality report |
| Baseline Model | 3 weeks | Baseline performance |
| Model Improvement | 4 weeks | Production-ready model |
| Deployment | 2 weeks | Model in production |
| Monitoring Setup | 1 week | Dashboards live |

## Risks

| Risk | Mitigation |
|------|------------|
| Data quality issues | Data validation pipeline |
| Model performance insufficient | Multiple algorithm approaches |
| Latency too high | Model optimization, caching |
```

## Best Practices

✅ **Version Everything**: Data, code, models, features
✅ **Automate Early**: CI/CD from start
✅ **Monitor Comprehensively**: Technical + business metrics
✅ **Start Simple**: Baseline model first
✅ **Reproducibility**: Track experiments meticulously
✅ **Cost Awareness**: Monitor GPU/inference costs
✅ **Gradual Rollout**: Canary deployments для models

## Common Pitfalls

❌ **Training-Serving Skew**: Different code paths
✅ Use same feature transformation code

❌ **Data Leakage**: Future data в training
✅ Strict temporal splits

❌ **No Monitoring**: Deploy and forget
✅ Comprehensive monitoring from day 1

❌ **Over-Engineering**: Building too much upfront
✅ Iterative, start with simple pipeline

## Success Criteria

- **Automated Pipeline**: End-to-end automation
- **Model Performance**: Meeting business targets
- **Latency**: <[X]ms p95
- **Cost Efficiency**: Within budget
- **Monitoring**: Comprehensive dashboards
- **Retraining**: Automated based on drift
