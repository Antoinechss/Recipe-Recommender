#!/bin/bash

# Activate Python 3.12 virtual environment (recommended for full functionality)
if [ -d ".venv-py312" ]; then
    echo "🐍 Using Python 3.12 environment for full functionality..."
    source .venv-py312/bin/activate
elif [ -d ".venv" ]; then
    echo "⚠️ Using Python 3.14 environment (limited functionality)..."
    source .venv/bin/activate
else
    echo "❌ No virtual environment found. Please run setup first."
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
if [ -d ".venv-py312" ]; then
    pip install -r requirements-full.txt
else
    pip install -r requirements.txt
fi

# Run Streamlit app
echo "🚀 Starting Recipe Recommender..."
streamlit run app/app.py
