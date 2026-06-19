# Recommended Project Structure

student-performance-indicator/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── artifacts/
│   ├── logs/
|
├── config/
│   ├── logging_config.yaml/
|
├── data/
│   ├── raw/
│   └── processed/
│
|── docs/
├── models/
│
├── notebooks/
│
├── scripts/
│   └── download_dataset.py
│
├── src/
|  |- upr/
|       ├── data/
|       ├── features/
|       ├── models/
|       └── evaluation/
│       └── utils/
├── tests/
│   └── sample_data/
│
├── environment.yml
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
