# ⏳ Quickstart Guide 

Quickstart development with these examples and tips to build, containerize, and deploy your own LLM service using best practices. This guide is designed to be generalizable to similar cloud/container/AI projects using the technologies. The sample project can be found from  [quickstart/KalevalaGPT](KalevalaGPT).

<details>
<summary>📁 Navigation</summary>

- [📝 Project Plan](#-project-plan)

1.  [Project layout and basic setup](#1-project-layout-and-basic-setup)

2. [Model development and exporting](#2-model-development-and-exporting)
 
3. [Implementing RAFT API](#3-implementing-raft-api)

4. [Full-stack app development](#4-full-stack-app-development)

5. [Containerizing the API with Docker](#5-containerizing-the-api-with-docker)

6. [Deploying the full-stack to Rahti](#6-deploying-the-full-stack-to-rahti-openshift)

7. [Next steps](#7-next-steps)

</details>

## 📝 Project Plan

Follow this full-stack chatbot service example on creating KalevalaGPT, a chatbot for answering questions about Kalevala, to get hands-on experience with Docker, Kubernetes, and HPC/cloud platforms like CSC Puhti, cPouta, and Rahti. Along the way, you’ll pick up crucial information and practical tips that you can apply to your own projects.

### Steps to building a full-stack chatbot service:

1. **Obtain** a language model and fine-tuning dataset

2. **Develop** training scripts for CSC Puhti

3. **Containerize** the model API

4. **Implement** the backend service for calling the API

5. **Design** and **build** the frontend interface

6. **Run** the full-stack app in Docker Compose

7. **Convert** the Docker Compose and API container configs into Kubernetes manifests to enable scaling

8. **Deploy** to Rahti (OpenShift) 

## 1. Project layout and basic setup


To support best practices with a clean and scalable workflow, the KalevalaGPT project will consist of the following structure:

    finetune/                   # For fine-tuning the model on a custom dataset
    ├── data/                   # Training data
    ├── finetune_model.py       # Fine-tuning script
    ├── config.yaml             # Parameters, paths, etc.
    ├── merge_export_model.py   # Export model
    └── jobs/                   # HPC batch jobs for Puhti
        ├── finetune_job.sh     # SLURM batch file for training
        └── export_job.sh       # SLURM batch file for export

    ai-model/                   # For model inference and RAFT
    ├── api/                    
    │   ├── app.py              # Flask API
    │   ├── rag.py              # Semantic retrieval implementation
    │   └── predict.py          # Load model with Hugging Face transformers, inference
    ├── storage/                # Vector database for RAG 
    │   ├── default__vector_store.json
    │   ├── docstore.json
    │   ├── graph_store.json
    │   ├── image__vector_store.json
    │   └── index_store.json
    ├── test/                   # For unit testing
    │   ├── __init__.py
    │   ├── predict_test.py
    │   └── rag_test.py
    ├── .env                    # For storing secrets
    ├── .gitignore
    ├── .dockerignore
    ├── requirements.txt        # Python API dependencies
    └── Dockerfile              # Set up API + runtime

    app/                        # Full-stack app files and docker setup
    ├── frontend/               # React frontend
    │   ├── src/
    │   ├── node_modules/
    │   └── package.json
    ├── backend/                # Node.js backend
    │   ├── server.ts
    │   ├── node_modules/
    │   ├── package.json
    │   └── .env                # For storing secrets
    ├── node_modules/
    ├── package.json
    └── .gitignore

    
## 2. Model development and exporting

This section explains how to fine-tune a model on Puhti, CSC’s high-performance computing (HPC) cluster, and then export it for later use.

>For more information about fine-tuning and other methods of customizing AI models, check out the document [Customizing behavior of pre-trained AI models](../ai-models/custom-models.md)

### 2.1: Connect to Puhti using SSH

1. In **MyCSC** (CSC’s online portal), add your SSH key. This allows your computer to connect to Puhti without typing a password every time.

2. Find your CSC username in your profile on MyCSC.

3. Open a terminal and connect:

    ssh <csc-username>@puhti.csc.fi

---

### 2.2: Prepare and copy the AI fine-tuning files

- Open `config.yaml` and edit `project_id` and `scratch_dir` to match your CSC project number (shown in MyCSC).

- Update `finetune_job.slurm` and `export_job.slurm` with your project ID.

**Slurm** is a job scheduler used on HPC systems. It manages resources and runs your training jobs on the cluster.

- Copy the training files from your computer to Puhti using **SCP** (Secure Copy Protocol):

        scp -i ~/.ssh/<sshkey> -r /path/to/folder/ai-trainer <csc-username>@puhti.csc.fi:~

---

### 2.3: Check that files were transferred

Navigate into the folder and list files:

    cd ai-trainer
    ls

---

### 2.4: Create and activate a Python environment

Python virtual environments keep dependencies isolated, so you don’t break other projects.

    module load pytorch          # Loads PyTorch (deep learning library) on Puhti
    python3 -m venv myenv        # Create a virtual environment
    source myenv/bin/activate    # Activate the environment

---

### 2.5: Install dependencies

Dependencies are listed in `requirements.txt`. Install them inside the environment:

    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate # Exits the virtual environment

---

### 2.6: Run the fine-tuning Slurm job

Submit the training job to Slurm:

    sbatch jobs/finetune_job.slurm

If successful, you’ll see something like:

    Submitted batch job 29281958

- Check job status:

        squeue -u your-username

- View output logs live:

        tail -f slurm-29281958.out

---

### 2.7: Export the model with llama.cpp

Once fine-tuning finishes, the model needs to be merged and exported.

`llama.cpp` is a lightweight C++ library that allows you to run LLaMA-family models efficiently on your own computer.

1. Go to your project’s scratch storage:

        /scratch/project_<project-number>
        git clone https://github.com/ggerganov/llama.cpp

2. Return to your user folder and run the export job:

        cd /users/<csc-username>/ai-trainer
        sbatch jobs/export_job.slurm

---

### 2.8: Download the model to your own computer

When export is done, the model will be at:

    /scratch/project_<project-number>/tinyllama-kalevala-chat.gguf


Use SCP to copy it back to your machine:

    scp -r <csc-username>@puhti.csc.fi:/scratch/project_<project-number>/tinyllama-kalevala-chat.gguf ./tinyllama-kalevala-gguf

---

Now you have a fine-tuned model that can be used on its own, or with improved performance using RAG (Retrieval Augmented Generation) implemented in the next step.

## 3. Implementing RAFT API

Once you have finished training the model using Puthi and have retrieved the `.gguf` model file, you can integrate it into a Retrieval-Augmented Generation (RAG) workflow.

>For a more in-depth example on setting up an AI API endpoint using Ollama, read [Creating an API endpoint for an AI model in CSC cPouta](../ai-models/README.md#-creating-an-api-endpoint-for-an-ai-model-in-csc-cpouta) 

You can use this Google Colab file to play around with the rag implementation which includes:

- Code to create a vector database using a pdf
- Vector index loading, persistence, and retrieval
- AI inference using the retrieved data

🔗 https://colab.research.google.com/drive/15vIIUE8J7y8AeKNeKIGL4F10BZIZucL6?usp=sharing

---

### 3.1: Move the project to a cloud or server instance

RAG requires running a service where the model can respond to queries. You can deploy it on a cPouta instance (or any other Linux server with sufficient CPU/GPU resources). The resources are copied to a VM with a xlarge flavor and Ubuntu-20.04 image:

    scp -i ~/.ssh/<ssh-key> -r /path/to/KalevalaGPT/ai-model ubuntu@<instance-ip>:~
    ssh -i ~/.ssh/<ssh-key> ubuntu@<instance-ip>

---

### 3.2: Set up the Python environment

To ensure all dependencies are isolated and reproducible:

    cd ai-model
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

- Python virtual environments (venv) prevent conflicts between project dependencies.

- Requirements file ensures that the exact versions of libraries (Flask, LlamaIndex, Transformers, etc.) are installed.

---
### 3.3: Understand how RAFT works in this project

RAFT uses RAG for retrieval and generation and adds fine-tuning on top:

1. Retrieval (Vector Database)

    - Documents (PDFs, text) are processed and stored as embeddings in a vector index.

    - Vector search allows the model to quickly find the most relevant pieces of context.

    - LlamaIndex handles creating the index, storing it persistently, and performing similarity-based retrieval.

2. Generation (Language Model)

    - The fine-tuned `.gguf` model from Puhti is loaded using `llama.cpp` for efficient inference.

    - When a query arrives, the model receives both the question and the retrieved context.

    - The output combines the model’s internal knowledge with the retrieved documents for more accurate and context-aware answers.

<p align="center"><img src="RAFT API sequence diagram.png" alt="RAFT API Workflow" width="700"/></p>

<p align="center"><em>RAFT API Workflow sequence diagram: Health check, retrieval-augmented generation, and answer delivery from the vector index to the user.</em></p>

---

### 3.4: Test individual components

Before we expose the API, we must verify that all modules work as expected:

    # Test the retrieval system
    python3 -m test.rag_test

    # Test model inference
    python3 -m test.predict_test

---

### 3.5: Run the Flask API

The Flask app exposes endpoints for health checks and queries:

    export FLASK_APP=api.app
    flask run --host 0.0.0.0 --port 8000

- `GET /health` Returns the server and model status.

- `POST /query` Sends the users question to the RAFT system and returns an answer, sources, and context.

Test the API with curl:

    curl http://localhost:8000/health
    curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question": "Who is Wainamoinen?"}'

---

Once everything works as expected, we are ready to move forward to the full-stack implementation.

## 4. Full-stack app development

Once the RAFT API is running and responding correctly, the next step is to build a full-stack application where the user communicates with the backend through the frontend which displays answers and allows user interaction. This section will guide you through implementing a **React** **TypeScript** frontend and a Node.js **TypeScript** backend. You can either use the one provided in the KalevalaGPT example, or follow the steps to create one yourself.

### 4.1: Initialize the project directories

Create separate directories for the frontend and backend to separate logic and allow independent deployment:

    mkdir frontend backend

### 4.2: Set up the frontend

Go to the frontend directory and initialize a React + TypeScript project using Vite:

    npm create vite@latest frontend     # Choose Framework: React, Variant: TypeScript
    cd frontend
    npm install

You can test the React + TS app with

    npm run dev

And after that, you can clean up the example app files in /src and leave just `main.tsx` and `App.tsx`. 

### 4.3: Understanding how the KalevalaGPT frontend works

1. Message structure

    - The `Message` interface defines each chat entry with universal fields (sender, text) and optional fields (`context`, `sources`) for bot responses and (`topK`, `similarityCutoff`) for user messages.

2. Input & queries

    - Users type their question in the input box and can adjust `top_k` and `similarity_cutoff` values before sending.

    - The message is appended to `messages` list after sending, and a fetch request is sent to the backend with the question and parameters.

3. UI updates

    - `useState` tracks `messages` so that any new message triggers a UI update.
    - `useRef` ensures the latest message scrolls into view automatically.

### 4.4: Set up the backend for local development

Initialize a Node.js project in the backend folder:

    cd ../backend
    npm init -y
    npm install express cors axios dotenv ts-node-dev typescript @types/node @types/express

We are using Axios as it simplifies the HTTP requests using promises and error handling. Express.js is used as the backend framework because it is lightweight and easy to expand on. CORS is enabled to allow the React frontend (which is running on a different port) to communicate with the API.

### Test the full app

Go to the main folder, and install concurrently to test run both the backend and frontend simultaneously with ease:

    npm install concurrently

Then add these to the main project folder's `package.json`:

    {
    "name": "kalevalagpt",
    "private": true,
    "scripts": {
        "dev": "concurrently \"npm run dev --prefix backend\" \"npm run dev --prefix frontend\""
    },
    "dependencies": {
        "concurrently": "^9.2.1"
    }
    }

## 5. Containerizing the API with Docker

Build the image with

    docker build -t kalevalagpt-ai . 

As the .env file is dockerignored, we need to add it into the run statement:

    docker run -d -p 8000:8000 --env-file .env kalevalagpt-ai 

## 6. Deploying the full-stack to Rahti (OpenShift)

Deploying software from a GitHub repository to CSC Rahti

CSC Rahti is a Platform-as-a-Service (PaaS) offering based on [Red Hat OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift), which enables you to deploy containerized applications directly from source code or pre-built container images.

### Pre-requisites:

- A GitHub repository containing your application code

- An OpenShift-compatible Dockerfile or [Source-to-Image](https://docs.redhat.com/en/documentation/openshift_container_platform/3.11/html/creating_images/creating-images-s2i) (S2I) compatible setup

---

### Deploy using the Rahti Web UI

1. Log in to Rahti:
    - In [MyCSC](https://my.csc.fi/), authenticate using your Haka credentials, create a project, and add Rahti into the active services
    - Go to the Rahti login page and log in

2. Create a new project:
    - In the OpenShift dashboard, click "Create Project". Give it a name and in the description, add the CSC project id in the format of `csc_project: 1000123`

3. Import your app from Git:
    - In your project, click “Add to Project” > “Import from Git”

    - Paste your GitHub repo URL (public or private with token access)

    - Click Show advanced Git options > add optional Git reference, Context Dir as frontend first, then do the same for backend, and add the Source Secret

4. Choose Builder Image (e.g. Python, Node.js, etc.) or your Dockerfile, in this example, Node.js 20 is used

5. Configure environment variables if needed, and for the frontend and backend make sure that the ports are set up correctly.

6. Deploy and expose:

    - Click Create, and OpenShift will automatically build and deploy your app

    - Go to Routes and find the external URL for your app

Remember to switch the frontend and backend urls from localhost to addresses from Rahti.

> For more detailed instructions, visit https://docs.csc.fi/cloud/rahti/

## 7. Next steps

Frontend:

- Learn how to use localStorage https://www.geeksforgeeks.org/javascript/javascript-localstorage/

- Learn tailwind css https://tailwindcss.com/

