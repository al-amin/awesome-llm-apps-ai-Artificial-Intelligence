# Install Miniconda or Anaconda

If you haven't already, install Miniconda or Anaconda.

# Initialize Conda

Open the Terminal app and run `conda init` to initialize Conda.

# Create a new environment

Create a new environment by running `conda create -n myenv python=3.11`. Replace "myenv" with the name of your choice.

# Activate the new environment

Activate the new environment by running `conda activate myenv`.

# Verify that Python 3.11 is installed

Verify that Python 3.11 is installed in the environment by running `python --version`.

# Install packages using Conda

You can now use this environment to install and manage packages using Conda. For example, you can run `conda install numpy` to install the NumPy library.

# Exit the environment

To exit the environment, run `conda deactivate`.

Note: If you are using a Mac with Apple Silicon (M1) processor, you may need to use the `--arch` flag when creating the environment to specify the architecture of the Python interpreter. For example, `conda create -n myenv python=3.11 --arch arm64`.

On Mac:

# Create a new environment

Run `conda create -n autogen-studio-py311 python=3.11` to create a new environment with Python 3.11.

# Activate the new environment

Activate the new environment by running `conda activate autogen-studio-py311`.

# Install Autogen Studio

Run `pip install autogenstudio` to install Autogen Studio.

# Start the UI

Run `autogenstudio ui --port 8080` to start the UI with port 8080.

# Create a new directory

Create a new directory using `autogenstudio ui --port 8080 --appdir newdir`.

# UI Model settings:

To use Ollama models, you can list them using `ollama list` (terminal). The first model listed is llama2:13b, with an empty or NULL API and a base URL of http://localhost:11434/v1. You can test the model by clicking "Test Model" in the UI, which should print "Model tested successfully". 
ref: [01_ollama_macos ](https://github.com/al-amin/ai-Artificial-Intelligence/tree/main/01_ollama_macos)

The second model listed is llava:13b, with a NULL API and a base URL of http://127.0.0.1:11434/v1.
