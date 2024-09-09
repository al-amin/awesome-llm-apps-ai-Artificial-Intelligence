#09.09.2024 - Installing Go and Fabric on Mac

## Installation Instructions

### Install Go using Homebrew

To install Go, run the following command:
```bash
brew install go
```bash
Verify that you've installed Go by opening a terminal and typing:

```bash$ go version```bash
Install Fabric
Make sure Go is installed, then run the following command to install Fabric directly from the repo:

```bashgo install github.com/danielmiessler/fabric@latest```bash
Run the setup to set up your directories and keys:

```bashfabric --setup```bash
Environment Variables
You may need to set some environment variables in your ~/.bashrc or ~/.zshrc file. For Apple Silicon based macs, add the following lines at the bottom of the file:
```bash
# Golang environment variables
export GOROOT=/opt/homebrew/bin/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH:
```bash
Usage
Once you have it all set up, here's how to use Fabric:
```bash
fabric -h
```bash
Examples
Here are some examples of what you can do with Fabric:

Run the summarize Pattern based on input from stdin. In this case, the body of an article:
```bash
pbpaste | fabric --pattern summarize
```bash
* Run the analyze_claims Pattern with the --stream option to get immediate and streaming results:
  ```bash
pbpaste | fabric --stream --pattern analyze_claims
```bash
