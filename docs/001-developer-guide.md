# Developer Guide

## clone repo

git clone [repo-name]

## enter repo folder

cd [repo-name]

## Create conda environment

conda create -n spi python=3.12

## activate conda environment

conda activate spi

## install dependencies and package

pip install -e ".[dev]"

## install pre-commit hooks

### Execute pre-commit before commit

pre-commit install 

### Execute pre-commit before push

pre-commit install --hook-type pre-push