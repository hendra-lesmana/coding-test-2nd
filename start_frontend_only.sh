#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================"
echo -e " RAG Frontend Server"
echo -e "========================================${NC}"
echo

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo -e "${RED}Error: frontend directory not found!"
    echo -e "Please run this script from the project root directory.${NC}"
    exit 1
fi

cd frontend

echo -e "${YELLOW}Installing dependencies...${NC}"
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}Error installing dependencies.${NC}"
    exit 1
fi

echo
echo -e "${GREEN}Starting Next.js development server...${NC}"
echo -e "${BLUE}Frontend will be available at: http://localhost:3000${NC}"
echo
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo

npm run dev
