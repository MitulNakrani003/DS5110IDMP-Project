#!/bin/bash

echo "🚇 Starting MBTA System..."

# Install requirements
echo "📦 Installing requirements..."
pip3 install -r req.txt

# Start API
echo "🚀 Starting API..."
cd API
python3 main.py &

# Wait a moment for API to start
sleep 3

# Start UI
echo "🎨 Starting UI..."
cd ../UI
streamlit run ui.py 