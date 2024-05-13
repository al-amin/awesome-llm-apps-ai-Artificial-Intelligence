# Ollama WebUI

Ollama WebUI is a self-hosted, feature-rich, and user-friendly WebUI that can operate entirely offline. It is compatible with various LLM runners, including Ollama and OpenAI-compatible APIs. For more detailed information, please refer to our [Ollama WebUI Documentation](https://github.com/open-webui/open-webui).

## Installation Guide 🚀

Please note that certain Docker environments may require additional configurations. If you encounter any connectivity issues, our detailed guide in the [Ollama WebUI Documentation](https://github.com/open-webui/open-webui) is ready to assist you.

## Quick Start with Docker 🐳

### Installation with Default Configuration
If Ollama is installed on your computer, run the following command:
```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

### If Ollama is Installed on a Different Server
To connect to Ollama on a different server, change the OLLAMA_BASE_URL to the server's URL:
```bash
docker run -d -p 3000:8080 -e OLLAMABASEURL=https://example.com -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```


### To Run Open WebUI with Nvidia GPU Support
Use the following command:
```bash
brew install --cask ngrok
```
