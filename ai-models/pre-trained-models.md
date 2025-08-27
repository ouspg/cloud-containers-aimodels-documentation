# Customizing behavior of pre-trained AI models

A guide to customizing the outputs of pre-trained models, whether they are run locally on your own hardware or accessed through a third-party API.

<details>
<summary>📁 Navigation</summary>

- [🧩 Adapting pre-trained models using context](#-adapting-pre-trained-models-using-context)

- [⌨️ Prompt engineering techniques](#️-prompt-engineering-techniques)

- [💡 Controlling AI API output using prompt engineering in Azure AI Foundry](#-controlling-ai-api-output-using-prompt-engineering-in-azure-ai-foundry)

</details>

## 🧩 Adapting pre-trained models using context

### Prompt engineering

Prompt engineering is the act of guiding generative AI models through prompts to help shape and bias outputs. As Large Language Models (LLMs) have a broad base set of knowledge, developers can significantly improve the accuracy and reliability of AI models by carefully structuring and optimizing the input prompts for specific tasks. Prompt engineering is usually performed through best practices and creativity, as well as trial and error, to make the AI model perform as expected. 

### Providing context documents

Supply relevant data as part of the input (prompt) when querying a model. The simplest and most flexible option to add extra knowledge for many use cases. E.g, providing a PDF document for a LLM to reference. 

### Retrieval-Augmented Generation (RAG)

Use a pre-trained model and add a dynamic search layer on top that retrieves documents at query time. Moderately easy to set up. No model training is needed, but requires building an effective retrieval system for data, for example, by using semantic retrieval.

## ⌨️ Prompt engineering techniques

A **prompt** refers to a natural language text that requests a generative AI model to elicit a response in the form of text, image, audio, or other formats. Not every prompt gives equal results from a generative AI model, which is why systematic designing of prompts through continuous testing and refining is required to get usable and repeatable results. 

**Instruction sets** (also called "system prompt", "instruction", "role", etc.) are instructions, guidelines and contextual information used as a basis to guide how the AI model is supposed to react to various kinds of prompts presented by the users. Prompt engineering an instruction set is important as it acts as a framework to generate relevant and contextually aware responses, as well as limit the user from performing unwanted tasks using the LLM (such as jailbreaking or outputting unwanted information like the instruction set).

### Best practices in prompt engineering

- **Write** clear and specific instructions 

    *Ensures that the AI understands the task, desired format, tone, and structure of the output. Optionally use formats like JSON, YAML, or Markdown to provide structure that AI models understand better*

- **Provide** enough context and examples

    *Share enough examples to enhance results and help AI tailor its response*

- **Place** the most relevant information first before sharing additional contextual information

    *Setting the task first can help produce better results. Consider using well-known prompt structures like COSTAR (Context, Objective, Style, Tone, Audience, and Response) as guidance*

- **Optimize** for few-shot learning

    *Try zero-shot or few-shot learning with effective, accurate, and unique examples before adding more*

- **Iterate** and **refine** the prompt

    *Refine the prompt through iteration and evaluate the results. Consider also testing different models, as each one excels at different fields*

Check out OpenAI's documentation on the best practices with prompt engineering: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api

>Also consider studying prompts of pre-existing ai tools like Lovable or VSCode Agent at https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools 

## 💡 Controlling AI API output using prompt engineering in Azure AI Foundry

In this tutorial, we will learn how to use Microsoft Azure AI Foundry to deploy an AI model, modify its system prompt, and use it through an API in a simple app.

### 1. Start by creating a new Azure AI Foundry

Create the resource in Azure Portal using default settings. Once it is deployed, click "Go to resource", and then "Go to Azure AI Foundry portal".

### 2. Pick an AI model

Next, we can go to the **Model catalog** to pick the AI model we want to use. For this tutorial, we will pick **gpt-4o** chat completion model. Clicking it and "Use this model" allows you to customize parameters like upgrade policy and limit token usage. Let's continue with the defaults by clicking "Deploy" 

### 3. Install the Azure OpenAI SDK:

Run this in a terminal:

    pip install openai

And make sure that both the openAI SDK and Python are installed in the same 

### 4. Try out the example

Copy the basic code sample from the "Get Started" section, add your API key from the "Endpoint" section, and try the app response.

You should see a response similar to:

    Paris is one of the most beautiful and culturally rich cities in the world. Here’s a curated list of must-see sights and activities to enjoy during your visit:

    ### **Iconic Landmarks**
    1. **Eiffel Tower**
    - No trip to Paris is complete without visiting this world-famous symbol of the city. Take an elevator or climb the stairs to one of the viewing platforms for spectacular views of Paris. The nighttime light show is a must-see! 

    2. **Louvre Museum**
    - The world’s largest art museum and home to the famous *Mona Lisa* and thousands of other masterpieces. Make sure to also admire the iconic glass pyramid at the entrance.

    ...


### 5. Change the system prompt

Try changing the "system" content to something else, e.g., "You are the least helpful travel agent." Now try re-running the code.

    Oh, Paris? Meh, it's just a big city with some old stuff lying around. I guess you could, like, wander aimlessly or maybe stare at the Eiffel Tower for a minute or two, if you're into tall metal structures. People also talk about the Louvre, but it's just a building full of paintings—one of them smiles a little. Sounds riveting, right?

    Other than that, I don't know—just walk around. Or don't. Whatever. Have fun figuring it out. Or not. Who cares, really?

See how the system responds in a way described in the system prompt. 

### 6. Go through more examples

Explore other examples and try different tech stacks from the dropdown menus at the top of the "Get Started" section.