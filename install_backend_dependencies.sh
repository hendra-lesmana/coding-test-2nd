#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " Installing Backend Dependencies"
echo -e "========================================${NC}"
echo

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo -e "${RED}Error: backend directory not found!"
    echo -e "Please run this script from the project root directory.${NC}"
    exit 1
fi

cd backend

echo -e "${CYAN}Installing Python dependencies for RAG Financial Q&A System...${NC}"
echo

echo -e "${YELLOW}Checking if virtual environment exists...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error creating virtual environment."
        echo -e "Please ensure Python 3.8+ is installed and in your PATH."
        echo -e "Download from: https://python.org${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Virtual environment created successfully${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

echo
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error activating virtual environment.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo

echo -e "${YELLOW}Installing Python packages...${NC}"
echo -e "${CYAN}Trying main requirements.txt...${NC}"
pip install -r ../requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Main requirements failed, trying minimal requirements...${NC}"
    pip install -r ../requirements-minimal.txt > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error installing Python dependencies."
        echo -e "Please check your internet connection and Python installation.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Minimal Python dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Full Python dependencies installed${NC}"
fi

echo
echo -e "${YELLOW}Checking if .env file exists...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created from template${NC}"
    else
        cat > .env << EOF
# RAG Financial Q&A System Configuration

# Choose one of the following API keys:
GEMINI_API_KEY=your_gemini_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here

# Vector Store Configuration
VECTOR_STORE_PATH=./vector_store
EOF
        echo -e "${GREEN}✓ .env file created with template${NC}"
    fi
    echo
    echo -e "${RED}IMPORTANT: Please edit backend/.env and add your API keys!${NC}"
    echo
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo
echo -e "${BLUE}========================================"
echo -e " BACKEND INSTALLATION COMPLETE!"
echo -e "========================================${NC}"
echo
echo -e "${GREEN}✓ Python virtual environment ready"
echo -e "✓ All Python dependencies installed"
echo -e "✓ Configuration file created${NC}"
echo
echo -e "${CYAN}NEXT STEPS:${NC}"
echo -e "${YELLOW}1. Edit backend/.env and add your API keys"
echo -e "2. Install frontend dependencies: ./install_frontend_dependencies.sh"
echo -e "3. Or install all at once: ./install_all_dependencies.sh"
echo -e "4. Run backend: ./start_backend_only.sh${NC}"
echo
read -p "Press Enter to exit..."
