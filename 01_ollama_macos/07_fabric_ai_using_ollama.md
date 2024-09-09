#09.09.2024 - Installing Go and Fabric on Mac

## Installation Instructions

### Install Go using Homebrew

`To install Go, run:`
```
brew install go
```
`Verify that you've installed Go by opening a terminal and typing:`
```
$ go version
```

### Install Fabric

`Make sure Go is installed, then run the following command to install Fabric directly from the repo:`
```
go install github.com/danielmiessler/fabric@latest
```
`Run the setup to set up your directories and keys:`
```
fabric --setup
```

## Environment Variables

You may need to set some environment variables in your `~/.bashrc` or `~/.zshrc` file. For Apple Silicon based macs, add the following lines at the bottom of the file:

```
# Golang environment variables
export GOROOT=/opt/homebrew/bin/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH:
```

## Usage

Once you have it all set up, here's how to use Fabric:

* `fabric -h`
Examples
Here are some examples of what you can do with Fabric:

* Run the summarize Pattern based on input from stdin. In this case, the body of an article:
  ```
pbpaste | fabric --pattern summarize
```

* Run the analyze_claims Pattern with the `--stream` option to get immediate and streaming results:
  ```
pbpaste | fabric --stream --pattern analyze_climits
```
