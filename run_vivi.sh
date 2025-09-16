#!/bin/bash
# Vivi Run Script

echo "🚀 Starting Vivi AI Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "📦 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
source venv/bin/activate

# Check if we're in WSL2
if grep -q Microsoft /proc/version; then
    echo "🐧 Running in WSL2 environment"
    echo "💡 Note: Some Windows-specific features will be limited"
    echo "   For full functionality, run this on Windows"
fi

# Run the application
echo "🎯 Launching Vivi..."
python -m src.main
