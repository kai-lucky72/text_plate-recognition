#!/bin/bash
# Quick Start Script for Printed Text Scanner

echo "================================"
echo "Printed Text Scanner - Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python version OK"
echo ""

# Check if Tesseract is installed
echo "Checking Tesseract OCR installation..."
tesseract --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠ Tesseract OCR not found!"
    echo "Install with:"
    echo "  - Linux (Ubuntu): sudo apt-get install tesseract-ocr"
    echo "  - macOS: brew install tesseract"
    echo "  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Tesseract found"
    tesseract --version | head -1
fi

echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "To start the application, run:"
echo "  python3 main.py"
echo ""
