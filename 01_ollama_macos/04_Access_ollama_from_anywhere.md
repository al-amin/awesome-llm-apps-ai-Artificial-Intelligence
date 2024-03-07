# Ollama from Anywhere

Welcome to Ollama! This guide will help you access Ollama from anywhere, even if it's running locally.

### Installing Ngrok

Before we begin, you'll need to install Ngrok, a reverse proxy tool that allows us to forward ports and access local applications remotely. You can download Ngrok for free from their website: <https://ngrok.com/>

On Mac, you can install Ngrok using the following command in your terminal:
```bash
brew install --cask ngrok
```
### Configuring Ngrok

Once installed, you'll need to sign up for a Ngrok account and obtain an Authtoken. You can do this by visiting the Ngrok website and clicking on the "Sign Up" button: <https://ngrok.com/>

After signing up, you'll be redirected to the Ngrok dashboard, where you can find your Authtoken. Copy this token and save it in a secure location.

Next, we need to add the Authtoken to our Ngrok configuration. To do this, run the following command:
```bash
ngrok config add-authtoken Your-Token
```
Replace "Your-Token" with your actual Authtoken.

### Serving Ollama with Ngrok

Now that we have Ngrok set up, let's serve Ollama using it. To do this, run the following command:
```bash
ollama serve
```
This will start Ollama and listen for incoming connections on port 11434. However, since we're running locally, we need to forward this port to Ngrok. To do this, run the following command:
```bash
ngrok http 11434 - to forward the port to ngrok
```
This will forward port 11434 from your local machine to Ngrok, allowing you to access Ollama remotely.

### Testing Ollama

To test Ollama, open a web browser and navigate to the following URL: <http://your-ngrok-url.com:11434>

Replace "your-ngrok-url" with the URL provided by Ngrok when you ran the `ngrok http` command. This should open Ollama in your web browser, even if it's running locally.

That's it! With these steps, you should now be able to access Ollama from anywhere, even if it's running locally. Happy coding!