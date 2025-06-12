#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " Installing Frontend Dependencies"
echo -e "========================================${NC}"
echo

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo -e "${RED}Error: frontend directory not found!"
    echo -e "Please run this script from the project root directory.${NC}"
    exit 1
fi

cd frontend

echo -e "${CYAN}Installing Node.js dependencies for RAG Financial Q&A System...${NC}"
echo

echo -e "${YELLOW}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js not found!"
    echo -e "Please install Node.js 16+ from: https://nodejs.org${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm not found!"
    echo -e "Please install Node.js 16+ from: https://nodejs.org${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js and npm are available${NC}"
echo -e "${CYAN}Node.js version: $(node --version)${NC}"
echo -e "${CYAN}npm version: $(npm --version)${NC}"
echo

echo -e "${YELLOW}Installing Node.js packages...${NC}"
npm install > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Error installing Node.js dependencies."
    echo -e "Please check your internet connection and Node.js installation.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js dependencies installed successfully${NC}"
echo

echo -e "${YELLOW}Verifying installation...${NC}"
if [ ! -d "node_modules" ]; then
    echo -e "${RED}Error: node_modules directory not created."
    echo -e "Installation may have failed.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Installation verified - node_modules directory exists${NC}"
echo

echo -e "${BLUE}========================================"
echo -e " FRONTEND INSTALLATION COMPLETE!"
echo -e "========================================${NC}"
echo
echo -e "${GREEN}✓ All Node.js dependencies installed"
echo -e "✓ Next.js development environment ready"
echo -e "✓ React and TypeScript configured${NC}"
echo
echo -e "${CYAN}NEXT STEPS:${NC}"
echo -e "${YELLOW}1. Install backend dependencies: ./install_backend_dependencies.sh"
echo -e "2. Or install all at once: ./install_all_dependencies.sh"
echo -e "3. Run frontend: ./start_frontend_only.sh"
echo -e "4. Run full application: ./start_app.sh${NC}"
echo
read -p "Press Enter to exit..."
