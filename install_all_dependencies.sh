#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " Installing All Dependencies"
echo -e " RAG Financial Q&A System"
echo -e "========================================${NC}"
echo

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo -e "${RED}Error: backend directory not found!"
    echo -e "Please run this script from the project root directory.${NC}"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo -e "${RED}Error: frontend directory not found!"
    echo -e "Please run this script from the project root directory.${NC}"
    exit 1
fi

echo -e "${CYAN}This script will install dependencies for both backend and frontend.${NC}"
echo
echo -e "${YELLOW}Requirements:"
echo -e "- Python 3.8+ installed and in PATH"
echo -e "- Node.js 16+ installed and in PATH${NC}"
echo
read -p "Press Enter to continue..."

echo
echo -e "${BLUE}========================================"
echo -e " STEP 1: Installing Backend Dependencies"
echo -e "========================================${NC}"
echo

cd backend

echo -e "${YELLOW}Checking if virtual environment exists...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error creating virtual environment."
        echo -e "Please ensure Python 3.8+ is installed and in your PATH."
        echo -e "Install from: https://python.org${NC}"
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

echo -e "${YELLOW}Installing Python dependencies...${NC}"
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

cd ..

echo
echo -e "${BLUE}========================================"
echo -e " STEP 2: Installing Frontend Dependencies"
echo -e "========================================${NC}"
echo

cd frontend

echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Error installing Node.js dependencies."
    echo -e "Please ensure Node.js 16+ is installed and in your PATH."
    echo -e "Download from: https://nodejs.org${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js dependencies installed successfully${NC}"

cd ..

echo
echo -e "${BLUE}========================================"
echo -e " INSTALLATION COMPLETE!"
echo -e "========================================${NC}"
echo
echo -e "${GREEN}✓ Backend dependencies installed (Python virtual environment)"
echo -e "✓ Frontend dependencies installed (Node.js packages)"
echo -e "✓ Configuration files created${NC}"
echo
echo -e "${CYAN}NEXT STEPS:${NC}"
echo -e "${YELLOW}1. Edit backend/.env and add your API keys:"
echo -e "   - Get Gemini API key: https://makersuite.google.com/app/apikey"
echo -e "   - Or get OpenAI API key: https://platform.openai.com/api-keys${NC}"
echo
echo -e "${YELLOW}2. Run the application:"
echo -e "   - Unix/Linux/macOS: ./start_app.sh"
echo -e "   - Or run services individually:"
echo -e "     * Backend: ./start_backend_only.sh"
echo -e "     * Frontend: ./start_frontend_only.sh${NC}"
echo
echo -e "${YELLOW}3. Access the application:"
echo -e "   - Frontend: http://localhost:3000"
echo -e "   - Backend API: http://localhost:8000"
echo -e "   - API Docs: http://localhost:8000/docs${NC}"
echo
read -p "Press Enter to exit..."
