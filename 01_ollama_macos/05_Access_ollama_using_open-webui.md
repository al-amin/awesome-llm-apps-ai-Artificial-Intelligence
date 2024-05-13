# Ollama WebUI

Ollama WebUI is a self-hosted, feature-rich, and user-friendly WebUI that can operate entirely offline. It is compatible with various LLM runners, including Ollama and OpenAI-compatible APIs. For more detailed information, please refer to our [Ollama WebUI Documentation](https://github.com/open-webui/open-webui).

## Installation Guide 🚀

First clone the repository using the following command:
```bash
git clone https://github.com/open-webui/open-webui.git
```

## Quick Start with Docker 🐳

### Installation with Default Configuration
If Ollama is installed on your computer, run the following command: ref (https://github.com/open-webui/open-webui?tab=readme-ov-file#installation-with-default-configuration)
```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

### If Ollama is Installed on a Different Server
To connect to Ollama on a different server, change the OLLAMA_BASE_URL to the server's URL:
```bash
docker run -d -p 3000:8080 -e OLLAMABASEURL=https://example.com -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```


### To access Open WebUI from browser
Open the browser and visit the following link:
```bash
[docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda](http://localhost:3000/auth/)
```
