To get started, clone the repository from GitHub by running the following command in your terminal:

```bash
git clone https://github.com/stackblitz-labs/bolt.diy
```

# Install Ollama
# Pull the latest qwen2.5-coder model
# Create a configuration file for the model following the instructions in the 'Modelfile'


create the new model
```bash
ollama create -f Modelfile qwen2.5-coder-latest-extra-ctx:14b
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
![64589](https://github.com/user-attachments/assets/a826406a-1c30-43b8-af8c-446a02529eca)


2. Run the Container:

```bash
docker-compose --profile development up
```

![75339](https://github.com/user-attachments/assets/a87898c1-bbc0-4eb4-8569-4ea113229431)

3. Access from the browser:
![9368](https://github.com/user-attachments/assets/790984ba-dddd-46fa-8651-2593ca73122e)


fix ollama issue: (access ollama from localhost:5173)

```bash
OLLAMA_ORIGINS=http://localhost:5173 ollama serve
```