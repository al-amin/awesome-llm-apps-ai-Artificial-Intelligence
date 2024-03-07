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
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/dd49724e-990b-43ad-a186-e55416618511)

This will start Ollama and listen for incoming connections on port 11434. However, since we're running locally, we need to forward this port to Ngrok. To do this, run the following command:
```bash
ngrok http 11434 - to forward the port to ngrok
```
![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/a950d89d-fd35-4728-bb4d-6053620a9701)



This will forward port 11434 from your local machine to Ngrok, allowing you to access Ollama remotely.

### Testing Ollama

To test Ollama, open a web browser and navigate to the following URL: <http://your-ngrok-url.com:11434>

Replace "your-ngrok-url" with the URL provided by Ngrok when you ran the `ngrok http` command. This should open Ollama in your web browser, even if it's running locally.

![image](https://github.com/al-amin/ai-Artificial-Intelligence/assets/2225839/5ac6ed2e-cad4-4a07-b568-a05986ed66e2)



Static Endpoint with ngrok
=====================================

Introduction
------------

In this guide, we will show you how to create a static endpoint for your application using ngrok. This will allow you to easily access your application from outside your local network.

Creating Endpoints
-------------------

First, you need to create endpoints for your application. To do this, follow these steps:

1. Go to the ngrok website and sign up for a free account.
2. Once you have an account, click on the "Create Endpoint" button.
3. Choose a name for your endpoint, such as "my-app".
4. Select the "Static" option.
5. Enter the URL of your application, such as "http://your_free_domain_.ngrok-free.app".
6. Click "Create Endpoint" to create the endpoint.

Creating Edges
----------------

Next, you need to create edges for your endpoint. To do this, follow these steps:

1. Go to the ngrok website and sign in to your account.
2. Click on the "Edges" tab in the top menu bar.
3. Click on the "Create Edge" button.
4. Select the endpoint you created earlier, such as "http://your_free_domain_.ngrok-free.app" and check the label for my-app.
5. Click "Create Edge" to create the edge.

Starting a Tunnel
-------------------

Now that you have created your endpoint and edge, you can start a tunnel from the command line. To do this, follow these steps:

1. Open your terminal or command prompt.
2. Copy and paste the following into your terminal:
```
ngrok tunnel --label edge=edghts_YOUR_EDGE http://localhost:11434
```
3. Press enter to start the tunnel.

Adding the Endpoint to Your Application
---------------------------------------
You can now access your application from outside your local network by going to the URL of your endpoint. For example, if you named your endpoint "my-app", you can access it at <https://your-free-domain-.ngrok-free.app>.


That's it! With these steps, you should now be able to access Ollama from anywhere, even if it's running locally. Happy coding!
