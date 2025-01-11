
Getting Started with Ollama on MacOS
=====================================

Ollama is a powerful tool for working with large language models locally, and it's easy to get started with on your Mac. Here are the steps to follow:

1. Download and Install Ollama
-------------------------------

First, download the Ollama app from the official website <https://ollama.com/download/Ollama-darwin.zip>. Once downloaded, unzip the app by double-clicking on the downloaded file.

2. Unzip and Move to Application Folder
----------------------------------------

After unzipping the Ollama app, you can move the Ollama app to your application folder.

3. Quickstart
--------------

To run and chat with Llama 2, follow these commands:

a. Run with DEBUG

`OLLAMA_DEBUG=1 ollama serve`

b. Run llama2:13b

`ollama run llama2:13b`

c. Run codellama:13b

`ollama run codellama:13b`

d. Run llava:13b

`ollama run llava:13b`

e. Check which port it's running on, Normally it's running on 127.0.0.1:11434.

`ollama serve`

f. Check the list of available models

`ollama list`

![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/8c08380e-9f42-4db7-b23e-9a920267fa58)


4. Upgrade all installed Ollama models:
--------------------------------------

Upgrade all installed Ollama models using command line:
`ollama list | tail -n +2 | awk '{print $1}' | xargs -I {} ollama pull {}`

For more information and to check the list of available models, refer to the official Ollama documentation <https://github.com/ollama/ollama>.

5. Access ollama from any application:
--------------------------------------
`OLLAMA_ORIGINS=* ollama serve`
OR `launchctl setenv OLLAMA_ORIGINS "*"`

6. Access ollama from any device from same network:
--------------------------------------
`launchctl setenv OLLAMA_HOST 0.0.0.0:11434`
ref: https://stackoverflow.com/questions/603785/environment-variables-in-mac-os-x AND
https://github.com/ollama/ollama/issues/703
