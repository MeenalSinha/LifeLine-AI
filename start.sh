#!/bin/bash

# LifeLine AI Quick Start Script

echo "🚨 LifeLine AI - Emergency Decision Support System"
echo "=================================================="
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -q -r requirements.txt

echo ""
echo "Starting LifeLine AI..."
echo ""
echo "📱 The application will open in your browser automatically"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

streamlit run lifeline_ai.py
