#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " RAG Backend Server"
echo -e "========================================${NC}"
echo

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo -e "${RED}Error: backend directory not found!"
    echo -e "Please run this script from the project root directory.${NC}"
    exit 1
fi

cd backend

echo -e "${YELLOW}Checking if virtual environment exists...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error creating virtual environment. Please check your Python installation.${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error activating virtual environment.${NC}"
    exit 1
fi

echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r ../requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Error with main requirements.txt, trying minimal requirements...${NC}"
    pip install -r ../requirements-minimal.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error installing dependencies.${NC}"
        exit 1
    fi
fi

echo
echo -e "${YELLOW}Checking if .env file exists...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
    fi
    echo
    echo -e "${RED}IMPORTANT: Please edit backend/.env and add your API keys!"
    echo -e "The file has been created from the template.${NC}"
    echo
    read -p "Press Enter to continue..."
fi

echo
echo -e "${GREEN}Starting FastAPI server...${NC}"
echo -e "${BLUE}Backend will be available at: http://localhost:8000"
echo -e "API Documentation will be available at: http://localhost:8000/docs${NC}"
echo
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
