#!/bin/bash

# Recipe Recommender Setup Script
# Sets up Python 3.12 environment for full functionality

echo "🍳 Recipe Recommender Setup"
echo "=========================="

# Check if Python 3.12 is available
if command -v python3.12 &> /dev/null; then
    echo "✅ Python 3.12 found"
    
    # Create virtual environment
    if [ ! -d ".venv-py312" ]; then
        echo "📦 Creating Python 3.12 virtual environment..."
        python3.12 -m venv .venv-py312
    else
        echo "✅ Python 3.12 virtual environment already exists"
    fi
    
    # Activate and install dependencies
    echo "🔧 Installing full dependencies..."
    source .venv-py312/bin/activate
    pip install --upgrade pip
    pip install -r requirements-full.txt
    
    echo ""
    echo "✅ Setup complete!"
    echo "🚀 Run the app with: ./run.sh"
    echo "📝 Or activate environment with: source .venv-py312/bin/activate"
    
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    echo "⚠️  Python 3.12 not found. Using Python $PYTHON_VERSION"
    echo "📝 Background removal will not be available"
    
    # Create basic virtual environment
    if [ ! -d ".venv" ]; then
        echo "📦 Creating virtual environment..."
        python -m venv .venv
    else
        echo "✅ Virtual environment already exists"
    fi
    
    # Activate and install basic dependencies
    echo "🔧 Installing basic dependencies..."
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo ""
    echo "✅ Setup complete (limited functionality)!"
    echo "🚀 Run the app with: ./run.sh"
    echo "📝 For full features, install Python 3.12"
    
else
    echo "❌ Python not found. Please install Python 3.12 or later."
    exit 1
fi
