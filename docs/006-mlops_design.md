# MLOps Design

## Status

Accepted

## Context

The Student Grade Prediction project requires a robust MLOps solution to ensure reproducibility, experiment tracking, artifact management, model versioning, deployment readiness, and governance throughout the machine learning lifecycle.

To achieve these goals, the project will use ZenML as the machine learning pipeline orchestration framework and MLflow as the experiment tracking and model management backend.

ZenML provides pipeline orchestration, artifact lineage, reproducibility, and workflow management, while MLflow provides experiment tracking, artifact storage, model packaging, and model registry capabilities.

## Decision

ZenML will be adopted as the primary MLOps framework for orchestrating machine learning workflows.

MLflow will be integrated with ZenML and used for:

* Experiment tracking
* Parameter logging
* Metric logging
* Artifact management
* Model logging
* Model versioning
* Model registry

All machine learning workflows must be executed through ZenML pipelines.

## Overall Model Process

The project workflow follows the Cross-Industry Standard Process for Data Mining (CRISP-DM).

```text
Business Understanding
        ↓
Data Understanding
        ↓
Data Preparation
        ↓
Modeling
        ↓
Evaluation
        ↓
Deployment
```

Within the project, the workflow is implemented as:

```text
Business Understanding
        ↓
Data Loading
        ↓
Data Validation
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Data Splitting
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Model Explainability
        ↓
Model Registration
        ↓
Deployment
        ↓
Monitoring
```

## Pipeline Orchestration

ZenML is responsible for orchestrating all machine learning workflows.

Responsibilities include:

* Pipeline execution
* Step dependency management
* Artifact lineage tracking
* Pipeline reproducibility
* Workflow standardization
* Integration with MLflow

Each stage of the workflow will be implemented as an independent and reusable ZenML step.

Example pipeline:

```text
Data Loading
    ↓
Data Validation
    ↓
Feature Engineering
    ↓
Data Splitting
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Model Explainability
    ↓
Model Registration
```

## Experiment Tracking

Experiment tracking will be performed using MLflow.

Information captured includes:

* Experiment name
* Run ID
* Start time
* End time
* Run status
* Training configuration
* Source code version

Experiment tracking enables reproducibility and comparison between multiple model runs.

## Parameters and Metrics Logging

All model parameters and evaluation metrics must be logged.

### Parameters

Examples include:

* Model type
* Learning rate
* Number of estimators
* Maximum tree depth
* Random seed
* Feature selection configuration

### Metrics

Examples include:

* RMSE
* MAE
* R² Score
* Training duration
* Inference duration

Metrics are used to compare model performance across experiments.

## Artifact Management

Artifacts generated during training and evaluation must be stored and tracked.

Examples include:

* Evaluation reports
* SHAP explanation reports
* Feature importance plots
* Data validation reports
* Model cards
* Training logs
* Dataset schema reports
* EDA reports

Artifacts will be generated locally and logged to MLflow for long-term storage and reproducibility.

## Artifact Lineage

ZenML will maintain artifact lineage across the entire pipeline.

Tracked artifacts include:

* Raw datasets
* Validated datasets
* Processed datasets
* Feature-engineered datasets
* Trained models
* Evaluation reports
* Explainability reports

Artifact lineage enables:

* Traceability
* Reproducibility
* Auditing
* Debugging

Every artifact must be traceable to the pipeline run that created it.

## Model Logging

Trained models will be logged using MLflow model packaging.

Benefits include:

* Standardized model storage
* Reproducible environments
* Dependency tracking
* Deployment readiness

Supported model types include:

* Scikit-learn
* XGBoost
* LightGBM
* Other MLflow-supported frameworks

## Autologging

Where appropriate, MLflow autologging will be enabled.

Automatically captured information includes:

* Parameters
* Metrics
* Models
* Training metadata

Manual logging may still be used for custom metrics and business-specific artifacts.

## Model Registry

MLflow Model Registry will serve as the source of truth for model versions.

Capabilities include:

* Version management
* Lifecycle management
* Promotion workflows
* Rollback support
* Production model tracking

Model lifecycle stages:

```text
Development
    ↓
Staging
    ↓
Production
    ↓
Archived
```

Only validated models may be promoted to Production.

## Reproducibility

All pipeline executions must be reproducible.

Reproducibility is achieved through:

* Version-controlled source code
* Fixed random seeds
* Logged parameters
* Versioned artifacts
* Registered models
* Tracked pipeline runs

Every model version must be traceable to:

* Source code version
* Dataset version
* Pipeline run
* Hyperparameter configuration

## Deployment and Serving

Deployment-ready models will be produced through the ZenML pipeline and registered in MLflow.

Deployment requirements include:

* Reproducible model packaging
* Version-controlled releases
* Registry-based model retrieval
* Automated deployment readiness checks

Models promoted to Production must satisfy predefined validation and performance requirements.

## Governance

The following information must be recorded for every production candidate model:

* Pipeline run ID
* Model version
* Dataset version
* Training timestamp
* Source code version
* Hyperparameters
* Evaluation metrics
* Validation results
* Explainability artifacts

No model may be promoted to Production without a complete audit trail.

## Consequences

### Positive

* Reproducible machine learning workflows
* Standardized pipeline execution
* Improved experiment tracking
* Improved model governance
* Artifact lineage visibility
* Easier collaboration
* Simplified deployment workflows
* Faster rollback and recovery

### Negative

* Additional infrastructure requirements
* Increased storage usage
* Additional operational complexity
* Learning curve for ZenML and MLflow
* Longer initial project setup time

## Future Enhancements

Potential future improvements include:

* Automated retraining pipelines
* CI/CD integration
* Data versioning
* Feature store integration
* Drift detection
* Monitoring and alerting
* Automated model promotion
* Containerized deployments
* Kubernetes-based serving infrastructure
* Canary deployments
* Blue-green deployments
