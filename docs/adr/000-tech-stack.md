# 000 Tech Stack

Status: Accepted 

## Context & Decision

We have standardized the core project environment on Python 3.12 managed via Conda. The ecosystem has been selected to establish a robust foundation for machine learning development, code quality, security, and testing. Every core package is version-locked to guarantee environment reproducibility across all development and production nodes.

### Component Breakdown & Justification

#### 📦 Runtime & Environment Management

* **Python 3.12**: The core runtime environment. It brings performance optimizations, improved error messages, and advanced typing features crucial for clean codebase maintenance.
* **Conda**: The environment and package manager. It ensures identical cross-platform replication of binaries and non-Python data science dependencies across development team machines.
* **`-e .` (Editable Package Mode)**: Links the local project directory as an editable package inside the environment. It enables clean absolute module imports and ensures that local code updates take effect instantly without re-installation.

#### 🤖 Data Science & Machine Learning Core

* **numpy == 2.3.1**: The foundational scientific computing library. It provides high-performance vector math capabilities, multi-dimensional array structures, and numerical routines.
* **pandas == 2.3.1**: The core data manipulation framework. It offers structured DataFrames optimized for data cleaning, aggregation, exploratory analysis, and time-series mutations.
* **scikit-learn == 1.7.1**: The primary machine learning library. It provides traditional predictive modeling algorithms, feature engineering processors, and pipeline validation tools.
* **matplotlib == 3.10.5**: The baseline data visualization library. It forms the architectural layer for generating static, animated, and interactive data charts.
* **seaborn == 0.13.2**: A statistical data visualization wrapper built on top of matplotlib. It streamlines the creation of complex, publication-ready statistical plots.
* **jupyter == 1.1.1**: The interactive prototyping environment. It allows engineers to conduct exploratory data analysis (EDA), visualize data, and experiment with models before committing code to production scripts.
* **ipykernel == 6.30.1**: The execution backend engine for Jupyter. It allows Jupyter notebook frontends to securely communicate with our specific Python 3.12 target kernel environment.

#### 🔬 Testing & Type Safety

* **pytest == 8.4.1**: The automated testing framework. It handles unit, integration, and functional test execution using simple syntax, fixtures, and powerful test-parametrization capabilities.
* **pytest-cov == 6.2.1**: A testing coverage extension plugin. It tracks and reports code coverage metrics during test execution to ensure newly added features are strictly verified.
* **mypy == 1.17.1**: The static type checker. It verifies optional Python type hints before runtime to eliminate data type errors and clarify variable schemas in data pipelines. Checks if your types make sense before running code
* **Pre-commit == 4.6.0**: This acts like an automated security guard for code repository. It intercepts code right before it is officially saved into Git history (the git commit step), checks it for errors, and blocks the commit if it finds any issues.

#### 🧼 Code Quality & Formatting

* **ruff == 0.12.8**: My Python error detector + cleanup tool. finds bugs, finds unused imports, finds bad patterns. checks style
* **black == 25.1.0**: fixes spacing, fixes indentation, fixes quotes, fixes line length

#### 🛠️ Utilities & System Configuration

* **python-dotenv == 1.1.1**: The environment variable parser. It securely isolates and injects configuration credentials, database keys, and configuration toggles from a local hidden `.env` file into runtime application environments.
* **tqdm == 4.67.1**: An extensible progress bar engine. It provides clean, low-overhead loop visualization readouts within scripts and notebooks for time-consuming data processing or model training sequences.

#### 🛡️ Security & Vulnerability Auditing

* **Bandit**: A static security analyzer. It scans source code for common security vulnerabilities, such as insecure function calls, hardcoded passwords, or improper file permissions.
* **pip-audit**: A dependency vulnerability scanner. It cross-references third-party packages against the Python Packaging Advisory Database to flag known security risks in external libraries before deployment.
