# 🤖 AI Models

This README contains guidelines for responsible use and deployment of machine learning and AI models:

<details>
<summary>📁 Navigation</summary>

- [✨ Should I use a pre-existing model, calibrate, or train one of my own?](#-should-i-use-a-pre-existing-model-calibrate-or-train-my-own)

- [Prompt engineering with pre-trained AI models](pre-trained-models.md) 

    - [🧩 Adapting pre-trained models using context](pre-trained-models.md#-adapting-pre-trained-models-using-context)
    
    - [⌨️ Prompt engineering techniques](pre-trained-models.md#️-prompt-engineering-techniques)
    
    - [💡 Controlling AI API output using prompt engineering in Azure AI Foundry](pre-trained-models.md#-controlling-ai-api-output-using-prompt-engineering-in-azure-ai-foundry)

- [Calibrating, fine-tuning, and training custom AI models](custom-models.md) 

    - [🧠 Customizing AI Models](custom-models.md#-customizing-ai-models)
    
    - [📊 Creating datasets](custom-models.md#-creating-datasets)
    
    - [🧙‍♂️ Fine-tuning TinyLlama for custom QA with PEFT and LoRA](custom-models.md#️-fine-tuning-tinyllama-for-custom-qa-with-peft-and-lora)
    

- [🦙 Creating an API endpoint for an AI model in CSC cPouta](#-creating-an-api-endpoint-for-an-ai-model-in-csc-cpouta)

- [📜 Data protection in AI systems](#-data-protection-in-ai-systems)
</details>

## ✨ Should I use a pre-existing model, calibrate, or train my own?

Deciding between choosing a pre-trained or a custom AI model can be confusing, especially if you are new to machine learning or are working on a unique and specific problem.

**Pre-trained models** are fast and very capable for most general tasks like content generation, summarization, classification, extraction, translation, and even code generation. They are continuously maintained and are easy to integrate into your web apps using their APIs. However, they offer only limited control over how they process requests and thus can result in improper results for niche tasks. Also questions regarding privacy and latency arise if they are being run in the cloud by a third party. Pre-trained models can be tailored to more specific needs using prompts within the limitations of their pre-existing datasets. 

>To learn more about using and customizing pre-trained AI models, read [`ai-models/pre-trained-models.md`](pre-trained-models.md) 


**Custom models** can be adapted in different ways depending on the goal and resources available. They can be calibrated to improve output quality for a specific subject, fine-tuned on your own data to better match a target use case, retrained with updated or expanded datasets, or fully trained from scratch for complete control.

**Calibration** and **Fine-tuning** give you better handling of a domain subject without needing to provide thousands of entries of training data. **Retraining** typically reuses the original model architecture and weights but updates it with new or expanded datasets to improve results.

**Fully training** a model from scatch gives you control over the model size, architecture, and output. Developing custom trained models requires the use of openly available datasets or data collection and processing, which is a tedious task.

>Find out more about calibrating and building custom models by heading to [`ai-models/custom-models.md`](custom-models.md) 

Before deciding on which route to choose, try the task with a general-purpose model (like ChatGPT or similar). Prompt engineering and some context can often produce results that are good enough, saving time and resources. Evaluate factors such as output accuracy, maintainability, and available resources to determine what fits your use case best.

## 🦙 Creating an API endpoint for an AI model in CSC cPouta

This tutorial covers using Ollama to deploy an HTTP API endpoint in CSC cPouta that runs `ollama serve` and exposes your model to `/api/generate`.

### 1. Create a VM in cPouta

Start by heading to [My CSC](https://my.csc.fi/login), create a new project, and add cPouta as a resource. Next, click the cPouta resource and log into the cPouta dashboard.

- Create a SSH key pair or use an existing one. Click **Compute > Key Pairs**, and add your public key.

- Click **Network > Security Groups**, add a new security group, and Allow SSH port `22` and HTTP port `11434` from `0.0.0.0/0`.

- Create a new instance in CSC cPouta in **Compute > Instances**

    - **Details:** Flavor: large (or bigger if your model requires more memory, there are also GPU accelerated versions available), Instance: Boot from image, choose `Ubuntu-22.04`. 
    - **Access & Security:** Make sure your Key Pair shows up, Select your created security group

Leave the rest as defaults and click Launch.

- Click **Network > Floating IPs**, then Allocate IP To Project. Click Allocate IP, and in Actions, click Associate and select your running instance. 

### 2. SSH into the new VM 

Once the VM is running and available through a public IP, in your own terminal, run: 

    ssh ubuntu@<your-vm-ip> -i <ssh-key-file>

### 3. Set up Ollama: 

Now that you have used SSH to access your instance, install Ollama:

    # Curl the install script and run it
    curl -fsSL https://ollama.com/install.sh | sh

    # Edit the Ollama service file
    systemctl edit ollama.service

Add host as `0.0.0.0` by adding the following lines to:

    ### Editing /etc/systemd/system/ollama.service.d/override.conf
    ### Anything between here and the comment below will become the new contents of the file

    [Service]
    Environment="OLLAMA_HOST=0.0.0.0"

    ### Lines below this comment will be discarded

Next, reload the systemd configuration and restart Ollama:

    systemctl daemon-reload
    systemctl restart ollama

### 4. Pull and run a LLM

Use the model of your choosing, or try e.g. the [`tinyllama-kalevala-chat`](https://ollama.com/nraesalm/tinyllama-kalevala-chat) model made in section [Custom models: 🧙‍♂️ Fine-tuning TinyLlama for custom QA with PEFT and LoRA](custom-models.md#️-fine-tuning-tinyllama-for-custom-qa-with-peft-and-lora)
:

    ollama pull nraesalm/tinyllama-kalevala-chat
    ollama run nraesalm/tinyllama-kalevala-chat

Curl the model to see if it responds:

    curl http://<public-ip>:11434/api/generate -d '{
        "model": "nraesalm/tinyllama-kalevala-chat",
        "prompt": "Who is Väinämöinen in Kalevala?"
    }'

If you get a response similar to this:

    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:39.839628064Z","response":"V","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:39.967288431Z","response":"ä","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.068517252Z","response":"in","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.167691033Z","response":"äm","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.266995331Z","response":"ö","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.365819292Z","response":"inen","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.464379892Z","response":" is","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.568692044Z","response":" the","done":false}
    {"model":"nraesalm/tinyllama-kalevala-chat","created_at":"2025-07-30T08:51:40.674947305Z","response":" most","done":false}

    ...

Your model is working correctly. To make the output usable, consider parsing the data first.

## 📜 Data protection in AI systems

Data protection is a critical concern in AI development, particularly if an AI system handles sensitive personal information.

### The core principles for AI data protection:

**1. Collect only what the system needs**

Limit the data to only relevant information that your AI model's specific functionality requires

**2. Anonymize data whenever possible**

Remove or replace identifying information so that individuals can't be identified

**3. Protect training data with access control, encryption and secure APIs**

Implement Role-Based Access Control (RBAC), add multi-factor authentication, and use the principle of least privilege

**4. Monitor the model responses and decision logic**

Document the model's decision-making process and test the model's reasoning logic thoroughly

---

### Compliance and legal considerations:

To make your AI systems secure and to comply with regulations and laws, **ensure** that data processing has a legal basis, **allow** the subjects to access, edit, and erase their data, and **develop** systems by integrating privacy considerations from the start. 

To learn more about data protection in the development and use of AI systems, read the article on the topic from tietosuoja.fi: https://tietosuoja.fi/en/ai-systems-and-data-protection

---

### AI system security and safety risks:

Avoiding common AI security threats can be avoided by following good principles for developing secure systems from the very start of development. The most common security risks for LLMs currently are prompt injections, sensitive information disclosure, and vulnerabilities in supply chains. 

You can learn more about the latest top 10 risks for generative AI by reading the OWASP GenAI Security Project for security and safety risks associated with generative AI technologies: https://owasp.org/www-project-top-10-for-large-language-model-applications/