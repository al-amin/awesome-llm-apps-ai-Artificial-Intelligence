#!/bin/zsh
# =========================================================
# Whisper Web Development Server Launcher
# =========================================================
# Author: AI Architect
# Date: June 12, 2025
# Description: Professional launcher for Whisper Web dev environment
# =========================================================

# Set strict error handling
set -e

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Define project paths
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_JSON="$PROJECT_ROOT/package.json"

# ASCII Art Banner
print_banner() {
  echo ""
  echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║${NC}                                                    ${BLUE}║${NC}"
  echo -e "${BLUE}║${NC}  ${GREEN}🎙️  WHISPER WEB - DEVELOPMENT SERVER${NC}             ${BLUE}║${NC}"
  echo -e "${BLUE}║${NC}  ${YELLOW}ML-powered speech recognition in the browser${NC}    ${BLUE}║${NC}"
  echo -e "${BLUE}║${NC}                                                    ${BLUE}║${NC}"
  echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
  echo ""
}

# Check system requirements
check_requirements() {
  echo -e "${BLUE}▶ ${NC}Checking system requirements..."
  
  # Check if Node.js is installed
  if ! command -v node &> /dev/null; then
    echo -e "${RED}✖ Node.js is not installed. Please install Node.js to run this application.${NC}"
    exit 1
  fi
  
  # Check Node.js version
  NODE_VERSION=$(node -v | cut -d 'v' -f 2)
  echo -e "${GREEN}✓ ${NC}Node.js version: ${GREEN}$NODE_VERSION${NC}"
  
  # Check if npm is installed
  if ! command -v npm &> /dev/null; then
    echo -e "${RED}✖ npm is not installed. Please install npm to run this application.${NC}"
    exit 1
  fi
  
  # Check npm version
  NPM_VERSION=$(npm -v)
  echo -e "${GREEN}✓ ${NC}npm version: ${GREEN}$NPM_VERSION${NC}"
  
  # Check if package.json exists
  if [ ! -f "$PACKAGE_JSON" ]; then
    echo -e "${RED}✖ package.json not found. Please run this script from the project root.${NC}"
    exit 1
  fi
  
  echo -e "${GREEN}✓ ${NC}All system requirements satisfied.\n"
}

# Verify dependencies are installed
verify_dependencies() {
  echo -e "${BLUE}▶ ${NC}Verifying project dependencies..."
  
  if [ ! -d "$PROJECT_ROOT/node_modules" ]; then
    echo -e "${YELLOW}! ${NC}Node modules not found. Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
      echo -e "${RED}✖ Failed to install dependencies.${NC}"
      exit 1
    fi
    echo -e "${GREEN}✓ ${NC}Dependencies installed successfully.\n"
  else
    echo -e "${GREEN}✓ ${NC}Dependencies already installed.\n"
  fi
}

# Print browser instructions
print_browser_instructions() {
  echo -e "${BLUE}▶ ${NC}Browser compatibility notes:"
  echo -e "  ${YELLOW}•${NC} Firefox users need to change the ${YELLOW}dom.workers.modules.enabled${NC}"
  echo -e "    setting in ${YELLOW}about:config${NC} to ${GREEN}true${NC} to enable Web Workers."
  echo -e "  ${YELLOW}•${NC} See GitHub issue #8 for more details.\n"
}

# Start development server
start_dev_server() {
  echo -e "${BLUE}▶ ${NC}Starting development server..."
  echo -e "  ${YELLOW}•${NC} Press ${YELLOW}Ctrl+C${NC} to stop the server at any time.\n"
  
  npm run dev
  
  if [ $? -ne 0 ]; then
    echo -e "\n${RED}✖ Development server failed to start or was terminated with an error.${NC}"
    exit 1
  fi
}

# Main execution flow
main() {
  print_banner
  check_requirements
  verify_dependencies
  print_browser_instructions
  start_dev_server
}

# Execute main function
main
