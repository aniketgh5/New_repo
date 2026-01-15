# Multi-App Docker CI/CD Deployment with Azure DevOps

This repository demonstrates an **end-to-end CI/CD pipeline** for deploying **multiple similar Python (Flask) applications** using **Docker images**, **Azure Container Registry (ACR)**, and **Azure App Service**.

The pipeline is designed to **detect changes automatically**, build and push Docker images selectively, and deploy them to corresponding Azure App Services.

---

## 📌 Overview

* Three applications: **appa**, **appb**, **appc**
* All applications share the **same Dockerfile structure** and deployment logic
* Azure DevOps pipeline dynamically:

  * Detects which app changed
  * Builds only required Docker images
  * Pushes images to ACR
  * Deploys to respective Azure App Services

---

## 🛠 Tech Stack

* **Language**: Python 3.11 (Flask)
* **Containerization**: Docker
* **CI/CD**: Azure DevOps Pipelines
* **Container Registry**: Azure Container Registry (ACR)
* **Hosting**: Azure App Service (Linux Containers)
* **OS**: Linux / WSL

---

## 📁 Repository Structure

```
.
├── appa/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── appb/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── appc/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── azure-pipelines.yml
└── README.md
```

---

## 🐳 Dockerfile (Common for All Apps)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

Each application runs a Flask server exposed on **port 5000**.

---

## ⚙️ Azure DevOps Pipeline – High-Level Flow

### 🔹 Trigger

* Runs on commits to `main`
* Triggered only when changes occur in:

  * `appa/**`
  * `appb/**`
  * `appc/**`
  * `azure-pipelines.yml`

---

## 🧠 Pipeline Stages Explained

### 1️⃣ Detect Stage

* Determines which applications changed using `git diff`
* Supports two modes:

  * **auto**: builds only changed apps
  * **manual**: builds selected apps via parameters
* Outputs a dynamic `components` variable

---

### 2️⃣ Build Stage

For each detected application:

* Logs in to Azure Container Registry
* Builds Docker image
* Tags image using pipeline parameter (`latest` by default)
* Pushes image to ACR

**Image Mapping:**

| Application | Docker Image |
| ----------- | ------------ |
| appa        | us11image    |
| appb        | us12image    |
| appc        | us13image    |

---

### 3️⃣ Deploy Stage

For each detected application:

* Updates Azure App Service container configuration
* Points App Service to the latest image in ACR
* Restarts the App Service

**Deployment Mapping:**

| Application | App Service Name |
| ----------- | ---------------- |
| appa        | demowebapp101    |
| appb        | demowebapp102    |
| appc        | demowebapp103    |

---

## 🔐 Configuration & Variables

The pipeline uses a **Variable Group**:

```
New variable group 14-Jan
```

Expected variables:

* `acrName`
* `acrLoginServer`
* `resourceGroup`

Azure service connection:

* `aniket_account`

---

## 🚀 Deployment Flow (Summary)

```
Code Push
   ↓
Azure DevOps Trigger
   ↓
Detect Changed Apps
   ↓
Docker Build
   ↓
Push Image to ACR
   ↓
Deploy to Azure App Service
```

---

## 🧪 Local Development (Optional)

```bash
cd appa
pip install -r requirements.txt
python app.py
```

Access locally:

```
http://localhost:5000
```

---

## ✅ Key Benefits of This Approach

* Selective builds (faster pipelines)
* Single pipeline for multiple applications
* Consistent Docker-based deployments
* Easy scalability (add new apps easily)
* Production-aligned CI/CD design

---

## 👤 Author

**Aniket Ghosh**
DevOps / Azure Engineer

---

## 📌 Notes

* All applications are intentionally similar to demonstrate **multi-app CI/CD design**
* This setup is suitable for **microservices-style deployments** using Azure App Service containers
* Can be extended to AKS or Helm with minimal changes
