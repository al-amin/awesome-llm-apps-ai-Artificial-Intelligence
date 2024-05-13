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
<img width="1452" alt="Screenshot 2024-05-13 at 19 29 59" src="https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/17ce9e0d-3cbc-42a6-8fc1-36b7dcc5a91e">

<img width="1387" alt="Screenshot 2024-05-13 at 19 32 31" src="https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/7a304655-127b-45d2-9973-7b88dfcff69a">


### To access Open WebUI from browser
Open the browser and visit the following link:
```bash
http://localhost:3000/auth/
```
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/2de4af47-af25-4915-b42f-928c0913183e)
