# Guidelines for the use of cloud services, container technologies, and AI models

Welcome! This project serves as a comprehensive, beginner-friendly guide for individuals or teams working with **cloud infrastructure**, **containerization**, and **AI model integration**. The aim of the document is to teach the basics of working with the technologies, and to provide practical workflows, examples, and best practices to help get started.

### 📁 Navigation
- [🎓 Free Dev Tools & Services for Students](#-free-dev-tools--services-for-students)
- [⏳ Quickstart Guide](#-quickstart-guide)
- [📦 Container Technologies](#-container-technologies)
- [📡 Cloud Computing](#-cloud-computing)
- [🤖 AI Models](#-ai-models)

---

## 🎓 Free Dev Tools & Services for Students

Useful free developer tools and services for containers, cloud, and AI+ML, available for free or with a student license:

- GitHub Student Developer Pack
- Cloud platforms
- Container Tools
- AI & Machine Learning

> Check out [`free-tools-services/README.md`](free-tools-services/README.md) for the full list.

---

## ⏳ Quickstart Guide

Quickstart development with these steps to build, containerize, and deploy your own AI model using best practices. This guide is designed to be generalizable to similar cloud/container/AI projects using the mentioned technologies.

- Project layout and basic setup
- Model development and exporting
- Containerizing with Docker
- Pushing to container registries
- Deploying to Rahti (OpenShift) or alternatives
- Best practices for portability and reusability

> Jump to [`quickstart/README.md`](quickstart/README.md) to get started.

---

## 📦 Container Technologies

This chapter documents the best practices, standards, and deployment workflows for containerized applications. Containers are lightweight, replicable environments that package your application code along with its dependencies. The following sections cover how to build efficient Docker images, secure your build process, and deploy to Kubernetes using local clusters:

- What are base images and containers?
- Development with Docker
- Dockerfile conventions
- Deployment with Kubernetes (k8s)

> Go to [`containers/README.md`](containers/README.md) to read more.

---

## 📡 Cloud Computing

Guidelines and best practices for working with cloud platforms:

- What are cloud services?
- Choosing the right Azure service type
- Other cloud providers
- Deploying a Docker Compose app to Azure Kubernetes Service (AKS)
- Deploying a Docker image to cPouta in CSC Cloud
- Cloud and web security essentials
- Data privacy and GDPR compliance

> See [`cloud/README.md`](cloud/README.md) for details.

---

## 🤖 AI Models

Guidelines for responsible use and deployment of machine learning and AI models:

- Should I use a pre-existing model or train my own?

- Prompt engineering with pre-trained AI models

    - Adapting pre-trained models using context
    - Prompt engineering techniques
    - Controlling AI API output using prompt engineering in Azure AI Foundry
    
- Calibrating, fine-tuning, and training custom AI models

    - Customizing AI models
    - Creating datasets
    - Fine-tuning TinyLlama for custom QA with PEFT and LoRA

- Creating an API endpoint for an AI model in CSC cPouta
- Data protection in AI systems

> Read [`ai-models/README.md`](ai-models/README.md) to learn more.