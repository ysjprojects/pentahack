# Pentahack

## Table of Contents
- [Pentahack](#Pentahack)
  - [Table of Contents](#table-of-contents)
  <!-- - [Project Overview](#project-overview) -->
  - [Requirements](#Requirements)
  - [Project Structure](#project-structure)
  - [Notes](#notes)
  <!-- - [Installation](#installation-/-usage) -->
  - [Usage](#usage)
  - [Minikube & Services](#minikube--services)
    - [Starting Minikube Kubernetes Cluster](#starting-minikube-kubernetes-cluster)
    - [Enabling MLOps Suite Services](#enabling-mlops-suite-services)
      - [Enabling model_deployer service](#enabling-model_deployer-service)
    - [Stopping Minikube Kubernetes Cluster](#stopping-minikube-kubernetes-cluster)

## Requirements
1. Python 3.8
2. 

## Project Structure
```
.
├── backend                 <- Flask backend
│   ├── Dockerfile          <- for dockerising Flask backend
│   ├── main.py
│   ├── 
│   └── sql                 <- contains sql scripts
└── docker-compose          <- docker compose file for MLOps Suite
```
