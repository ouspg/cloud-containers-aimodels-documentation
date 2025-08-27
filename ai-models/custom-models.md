# Calibrating, fine-tuning, and training custom AI models

For when just using pre-trained models is not enough. Contains documentation and examples on ways to calibrate, fine-tune, retrain, and fully train models from scratch, along with best practices on building and using datasets.

<details>
<summary>📁 Navigation</summary>

- [🧠 Customizing AI Models](#-customizing-ai-models)

- [📊 Creating datasets](#-creating-datasets)

- [🧙‍♂️ Fine-tuning TinyLlama for custom QA with PEFT and LoRA](#️-fine-tuning-tinyllama-for-custom-qa-with-peft-and-lora)

</details>

---

When browsing for different AI models to use, it is important to distinguish the extent to which the model has been trained. There is no standardization between terms of variants, but the following abbreviations/labels are the most commonly used:

- **Base model**: This model has only gone through the pretraining phase. Contains a knowledge base but cannot provide consistent answers even with careful prompting and requires fine-tuning to be usable. Good choice if you want to train using your own custom template and you have a lot of data to train with.

- **Instruct**, **Chat**: Pre-training and supervised fine-tuning have been performed on the model. Capable of chatting with users without the need for additional fine-tuning. Useful for further fine-tuning when you don't have a lot of data to use and want to utilize the pre-existing capabilities. 
Remember to format your dataset using the same structure as the original data that the model was trained on!

- **Multi-modal**, **Vision**: Can process multiple data types, such as text, images, audio, and video input. Some models can also generate images, audio, and video in addition to interpreting them. Usually has higher compute requirements than LLMs.

- **GGUF**: Generic GPT Unified Format. Used for efficiently storing and deploying LLMs by reducing model size and compute resource requirements through compression and quantization. Not suitable for fine-tuning!

## 🧠 Customizing AI Models

Customizing an AI model allows you to tailor its behavior and output to your specific needs, either through calibration, fine-tuning, retraining or by training from scratch. The approach you choose to train your model depends on the task, available data, and your technical experience.

### Model calibration

Calibrating refers to adjusting the output behavior of an AI model without making changes to its knowledge base or internal weights. The goal is to align the model's observed confidence scores (numerical estimates on how sure the model is about its predictions) and behavior with the predicted confidence through iterative processes. 

Calibration increases the reliability of the model's predictions while also reducing biases, hallucinations, and overconfidence or underconfidence. Common techniques include temperature scaling, Platt scaling, isotonic regression, or adjusting logit bias. 

### Fine-tuning an existing model

Take a pre-trained model and add new knowledge with your own dataset on top of the existing model knowledge. Offers a good compromise between performance and resource cost, and requires a smaller collection of labeled data as well as knowledge about how the model accepts datasets. 

Information on how to format data correctly for the specific model used is usually present somewhere in the model's documentation. E.g. the `TinyLlama1.1b-Chat` model from the open-source Tinyllama project uses the following format:

    "<|im_start|>user\n{['prompt']}<|im_end|>\n<|im_start|>assistant\n{['response']}<|im_end|>\n"


Even smaller models, when fine-tuned on high-quality data, can outperform larger general-purpose models on narrow tasks.

>If you're interested in combining fine-tuning with context-aware search for better domain adaptation, take a look at [RAFT (Retrieval-Augmented Fine-Tuning)](https://techcommunity.microsoft.com/blog/aiplatformblog/raft-a-new-way-to-teach-llms-to-be-better-at-rag/4084674).

### Model retraining

Retraining involves updating a trained machine learning model with fresh new data. It does not change any parameters or model architecture but overwrites old data with new entries to produce accurate predictions. Retraining is required when a model is experiencing [model drift](https://www.ibm.com/think/topics/model-drift).

### Training from scratch

Training a model from scratch means initializing a model with random weights and training it entirely on your own dataset and architecture, without using any pre-trained models or prior knowledge. This approach is used when there exists no pre-trained models for the domain, or the use case is highly specialized and unique. 

>Training from scratch requires large datasets and serious compute resources. Due to the scale and difficulty, this approach should not be the first choice in most cases.

## 📊 Creating datasets

AI model training requires access to a vast amount of diverse and high quality data. Datasets contain training data used to teach machine learning or computer vision algorithms on how to process information. Training data can be comprised of e.g. labeled text, images, or videos. These models interpret the data and improve their accuracy and perfomance when faced with new data.

High quality data is essential for successful machine learning, as it is directly proportional to the quality of the output. Quality and quantity of data affects the model's learning accuracy to produce appropriate results. 

---

### Qualities of a well-designed dataset:

- Data is **curated** and **relevant** to the use case, no unnecessary or broken data is present

- Data contains entries that the model would **expect** to face after deployment

- All entries are **unique**, no duplicates or unnecessary repetiton

- Data is **high quality** and **labeled** carefully, and confirmed that the label it **matches** the content of the entry

- **Similar** entries are **separated** from each other, back-to-back entries regarding the same topic can affect training negatively

- Data is gathered from **multiple sources** to avoid bias

- Dataset is **maintained regularly** to avoid data drift

---

### Why size matters?

Model calibrating and training isnt an exact science. The amount of data required depends factors such as model size, complexity and the specific task it is designed for.

Typically, for fine-tuning tasks, datasets ranging from around 1000 to 10000 examples can be sufficient but the optimal size depends heavily on the base model, the task complexity, and the diversity of topics covered.

For training a model from scratch or performing full model training, a common strategy is to follow the 10 times rule, which states that there should be at least ten times as many data instances as there are data features when training. For example, if you are training a 1b parameter LLM, the ideal training dataset should be around 10b in token size. 

The most practical approach is to start with a small dataset and identify any issues early, after which the dataset size can be increased gradually while evaluating the performance. This helps find the point at which the model's learning converges.

---

### Where to find data

Before deciding on creating your own dataset from scratch, its a good idea to look online for pre-made datasets on sites like [Google Dataset Search](https://datasetsearch.research.google.com/) or [Hugging Face Datasets](https://huggingface.co/datasets). 

Web crawling is a process where large amounts of data are collected from the internet and processed to a uniform format to be used in e.g. AI models. One of the most extensive sources of web crawl data is [CommonCrawl](https://commoncrawl.org/), an open repository of web crawl data from over 250 billion pages that is updated periodically each month.

Hugging Face has released a cleaned and refined version of Common Crawl, a 15-trillion token dataset for LLM pretraining called [FineWeb](https://huggingface.co/spaces/HuggingFaceFW/blogpost-fineweb-v1 ). FineWeb is specifically designed for large language model pretraining, and has been used as a resource to train most mainstream LLMs.

For testing purposes, LLMs can also be used relatively effectively to produce mock text-based datasets for fine-tuning. This is a useful approach for finding the correct formatting or labeling for niche topics where pre-made and fitting datasets are hard to find or manipulating raw data is tedious. Generating e.g. question-answer pairs can be done in small batches by prompting 10-20 entries at a time to keep the entries information-rich. Validity and formatting has to be checked thoroughly though, as AI can hallucinate incorrect data to poison the dataset.

## 🧙‍♂️ Fine-tuning TinyLlama for custom QA with PEFT and LoRA

In this example, we demonstrate how to fine-tune a conversational AI model using the Hugging Face Transformers library, the PEFT (Parameter-Efficient Fine-Tuning) framework, and the LoRA (Low-Rank Adaptation) method. Our goal is to train a small, efficient language model for Question Answering (QA) about the Finnish national epic, Kalevala using a small dataset.

We will start with the 1.1 billion parameter LLaMA model [`TinyLlama/TinyLlama-1.1B-Chat`](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat) that is fine-tuned for chat. The small model provdes a lightweight but capable starting point for the purpose while being fast to experiment with.

The small [`kalevala-dataset`](https://huggingface.co/datasets/nraesalmi/kalevala-dataset) consists of 330 prompt-response pairs in JSONL format, and includes details about the characters, events, and themes of Kalevala, as well as its significance in Finnish culture.

---

### Important technologies used in the example:

- **[Hugging Face Transformers](https://huggingface.co/docs/transformers/index) library**

    The Hugging Face Transformers library is a popular open-source library for working with state of the art pre-trained AI models for text generation, question answering, sentiment analysis, translating, etc. It supports popular frameworks like PyTorch and TensorFlow, and includes tools for tokenization, model conversion, and deployment.

- **`TinyLlama-1.1B-Chat` LLM**

    TinyLlama is a 1.1B parameter model inspired by LLaMA, trained from scratch to be lightweight and efficient for conversational tasks. Being a Chat-model, it has already been trained on language patterns and general knowledge to enable conversing with users.

    >Note! Small models like `TinyLlama` can produce varying results with fine-tuning due to their size and sensitivity to parameters. It's useful to prototype workflows and parameters on them before switching to a larger model that uses the same architecture like `Llama2` once the right fine-tuning parameters have been found. Parameters often need small re-adjustments after scaling up.

- **[PEFT (Parameter-Efficient Fine-Tuning)](https://github.com/huggingface/peft)**

    This library makes fine-tuning models resource-efficient by only updating only a small subset of parameters, such as adapters or LoRA weights, rather than the full model. This significantly reduces the GPU memory usage, training time and required storage.

    **[LoRA (Low-Rank Adaptation)](https://huggingface.co/docs/peft/en/package_reference/lora)** is a technique that enables efficient fine-tuning by injecting trainable low-rank matrices to existing weights. Instead of updating the full weight matrices, a low-rank decomposition is trained and added on top of the original weights as layers during fine-tuning. This drastically reduces the number of trainable parameters and reduces resource usage simultaneously.

-  **[Safetensors](https://huggingface.co/docs/safetensors/en/index)**

    Safetensors is a fast and secure binary format for loading model weights. It protects you from code execution vulnerabilities by using a strictly data-only format, unlike PyTorch's default which uses `pickle`. It’s safer for sharing, especially when downloading models from the internet.

---

### Comparing the capability of answering questions about Kalevala 

Trying to ask the non-tuned TinyLlama chat LLM about Kalevala gives a completely incorrect answer:

    $ ollama run tinyllama:chat
    >>> tell me about the author of Kalevala
    Kalivala is a poetry collection by poet and essayist A.P. C. 
    Devanadhaar, commonly known as "A.S. Namboothiri." The book was 
    first published in 1968 by the Collectors' Press of India and 
    has since become one of the most popular and celebrated 
    collections of Tamil poetry in Tamil Nadu and abroad.
    ...

After fine-tuning with the Kalevala dataset, the adapted model produces accurate and relevant answers:

    $ ollama run tinyllama-kalevala-chat
    >>> tell me about the author of Kalevala
    Kalevala is the epic poem of Finland written by Elias Lönnrot 
    in the 19th century. It narrates the history and folklore of 
    Finnish ancestors, emphasizing mythical heroes, natural 
    elements, and spiritual powers. Lönnrot collected thousands of 
    oral stories from rural communities across Karelia. 
    ...

---

### Try it yourself

For this tutorial, we demonstrate fine-tuning using Google Colab’s Python Notebooks, which provide free access to NVIDIA T4 GPUs. You can use the free version of Colab by logging into Google Drive using a Google account. To use the T4 GPUs in Colab, click "Runtime", "Change runtime type", and choose T4.

You can try the full training pipeline and experiment with the Kalevala assistant in this Colab notebook:

[\<Click here to go the the colab notebook\>](https://colab.research.google.com/drive/13f9OmCbazfQ4lydEeBXS9PRSVqVOYvpI?usp=sharing)
