# CI Pipeline

## Context

Its primary purpose is to act as an automated gatekeeper: every time a developer opens a Pull Request to merge code into the main branch, GitHub boots up a virtual server, installs the entire Python 3.12 stack, and runs all quality, testing, and security tools to ensure no broken or insecure code enters production.

## Features

### ⚡ Automated Integration Features

* **Automated Pull Request Triggers**: Executes automatically on every code change targeting the `main` branch.
* **Ephemeral Linux Runtime Environment**: Spins up clean, isolated `ubuntu-latest` cloud servers for every run.
* **Fast Dependency Caching**: Caches installed Python packages using `cache: pip` to accelerate subsequent workflow executions.
* **Matrix Build Architecture**: Features a strategy matrix config currently locked to testing on Python 3.12.

### 🧼 Static Code Analysis Features

* **Linter Code Guard**: Uses `ruff check` to catch code anti-patterns, logical flaws, and unused code imports.
* **Deterministic Style Enforcement**: Uses `black --check` to block any code that deviates from code style rules.
* **Static Type Verification**: Implements strict compile-time type verification across your `src` directory using `mypy`.

### 🧪 System Testing Features

* **Unit and Functional Test Suites**: Runs your entire testing layout in the `tests/` directory natively using `pytest`.
* **Test Coverage Profiling**: Automatically tracks code execution coverage metrics and compiles it into a standard XML output report file.

### 🛡️ Cybersecurity & Audit Compliance Features

* **Source Vulnerability Detection**: Uses `bandit -r` to scan local application files for critical exploits, security weaknesses, or accidental code vulnerabilities.
* **Supply Chain Package Auditing**: Scans third-party libraries using `pip-audit` against vulnerabilities to flag unpatched external packages before deployment.
