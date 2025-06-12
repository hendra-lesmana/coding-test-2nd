#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " RAG-based Financial Q&A System"
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

echo -e "${GREEN}Starting both Backend and Frontend...${NC}"
echo
echo -e "${YELLOW}Backend will be available at: http://localhost:8000"
echo -e "Frontend will be available at: http://localhost:3000"
echo -e "API Documentation: http://localhost:8000/docs${NC}"
echo
echo -e "${BLUE}Press Ctrl+C to stop both services${NC}"
echo

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}Stopping services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Services stopped.${NC}"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${GREEN}Starting Backend...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error creating virtual environment. Please check your Python installation.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error activating virtual environment.${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
pip install -r ../requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Trying minimal requirements...${NC}"
    pip install -r ../requirements-minimal.txt > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error installing dependencies.${NC}"
        exit 1
    fi
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${RED}IMPORTANT: Please edit backend/.env and add your API keys!${NC}"
    fi
fi

# Start backend in background
uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &
BACKEND_PID=$!

cd ..

# Start frontend
echo -e "${GREEN}Starting Frontend...${NC}"
cd frontend

# Install dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
npm install > /dev/null 2>&1

# Start frontend in background
npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!

cd ..

# Wait for services to start
echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 5

# Check if services are running
if kill -0 $BACKEND_PID 2>/dev/null && kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${GREEN}✓ Both services are running!${NC}"
    echo
    echo -e "${BLUE}Opening application in browser...${NC}"
    
    # Try to open browser (works on most systems)
    if command -v xdg-open > /dev/null; then
        xdg-open http://localhost:3000
    elif command -v open > /dev/null; then
        open http://localhost:3000
    else
        echo -e "${YELLOW}Please open http://localhost:3000 in your browser${NC}"
    fi
    
    echo
    echo -e "${GREEN}Application is ready!${NC}"
    echo -e "${BLUE}Press Ctrl+C to stop both services${NC}"
    
    # Wait for user to stop
    wait $BACKEND_PID $FRONTEND_PID
else
    echo -e "${RED}Error: One or both services failed to start${NC}"
    cleanup
fi
