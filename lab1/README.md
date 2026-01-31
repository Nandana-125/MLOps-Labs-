# Lab 1 - Dockerized ML Training (Wine + Logistic Regression)

This lab trains a Logistic Regression classifier on the sklearn Wine dataset,
then saves(Dockerlab/lab1):
- `wine_model.pkl` (trained model)
- `metrics.json` (accuracy + classification report)

## Build the Docker image
From the repo root:

```bash
docker build -t lab1-wine:v1 ./lab1

