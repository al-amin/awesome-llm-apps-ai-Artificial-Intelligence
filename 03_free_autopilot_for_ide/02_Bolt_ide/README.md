To get started, clone the repository from GitHub by running the following command in your terminal:

```bash
git clone https://github.com/stackblitz-labs/bolt.diy
```

# Install Ollama
# Pull the latest qwen2.5-coder model
# Create a configuration file for the model following the instructions in the 'Modelfile'


create the new model
```bash
ollama create -f Modelfile qwen2.5-coder-latest-extra-ctx:7b
```

![18443](https://github.com/user-attachments/assets/5487c0a2-f3b5-40aa-85dd-1792c21fa668)

![69605](https://github.com/user-attachments/assets/1bcf1ab0-9d01-48a5-b071-b831c24c8f48)



Now run the following command to install docker on your system(mac m1):

```bash
brew install --cask docker
```

Steps:
1. Build the Docker Image:

```bash
# Using npm script (I have used this one):
npm run dockerbuild

# OR using direct Docker command:
docker build . --target bolt-ai-development
```

2. Run the Container:

```bash
docker-compose --profile development up
```