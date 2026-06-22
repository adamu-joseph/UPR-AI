# MLOps Design

## Status

Accepted

## Context

The Student Grade Prediction project requires a robust MLOps solution to ensure reproducibility, experiment tracking, model versioning, deployment readiness, and governance throughout the machine learning lifecycle.

The project will use MLflow as the primary MLOps platform because it provides integrated support for experiment tracking, artifact management, model packaging, model registry, and deployment workflows.

## Decision

MLflow will be adopted as the standard MLOps framework for the project.

All training runs, evaluation results, model artifacts, and deployment-ready models will be tracked and managed through MLflow.

## Model Tracking

Model tracking will be performed using MLflow.

The following capabilities will be utilized:

### 1. Experiment Tracking

Track all training runs and maintain historical records of experiments.

Information captured includes:

- Experiment name
- Run ID
- Start and end times
- Run status
- Source code version
- Training configuration

### 2. Parameters and Metrics Logging

All model parameters and evaluation metrics must be logged.

Examples:

#### Parameters

- Model type
- Learning rate
- Number of estimators
- Maximum tree depth
- Random seed

#### Metrics

- RMSE
- MAE
- R² Score
- Training duration
- Inference duration

### 3. Artifact Management

Store files generated during training and evaluation.

Examples:

- Evaluation reports
- SHAP explanation reports
- Feature importance plots
- Data validation reports
- Model cards
- Training logs
- Dataset schema reports

Artifacts will be generated locally and logged to MLflow for long-term tracking and reproducibility.

### 4. Model Logging

Trained models will be logged using MLflow model packaging.

Benefits include:

- Standardized model format
- Reproducible environments
- Dependency tracking
- Easier deployment

Supported model types include:

- Scikit-learn
- XGBoost
- LightGBM
- Other MLflow-supported frameworks

### 5. Autologging

Where appropriate, MLflow autologging will be enabled to automatically capture:

- Parameters
- Metrics
- Model artifacts
- Training metadata

Manual logging may still be used for custom metrics, reports, and business-specific metadata.

### 6. Model Registry

MLflow Model Registry will serve as the source of truth for model versions.

Each registered model will support:

- Versioning
- Lifecycle management
- Promotion workflows
- Rollback capability

Typical lifecycle stages:

```text
Development
    ↓
Staging
    ↓
Production
    ↓
Archived