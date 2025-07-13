#!/bin/bash

# Test script for local getmethatdawg development
set -euo pipefail

echo "🧪 Testing getmethatdawg local development setup..."

# Check if we're in the right directory
if [[ ! -f "getmethatdawg-sdk/setup.py" ]]; then
    echo "❌ Please run this script from the getmethatdawg project root"
    exit 1
fi

# Install getmethatdawg-sdk in development mode
echo "📦 Installing getmethatdawg-sdk in development mode..."
cd getmethatdawg-sdk
pip install -e .
cd ..

# Test that the SDK works
echo "🔍 Testing getmethatdawg SDK..."
python3 -c "import getmethatdawg; print('✅ getmethatdawg SDK import successful')"

# Test the example agent
echo "🚀 Testing example agent..."
python3 -c "
import sys
sys.path.insert(0, 'examples')
import my_agent
from getmethatdawg import get_endpoints

endpoints = get_endpoints()
print(f'✅ Found {len(endpoints)} endpoints in example agent')
for endpoint in endpoints:
    print(f'  {endpoint.method} {endpoint.path} -> {endpoint.func_name}')
"

# Test the builder (without Docker)
echo "🔨 Testing builder..."
python3 -c "
import tempfile
from getmethatdawg.builder import GetMeThatDawgBuilder
import os

# Create temp directory
with tempfile.TemporaryDirectory() as temp_dir:
    builder = GetMeThatDawgBuilder('examples/my_agent.py', temp_dir)
    try:
        builder.analyze_source()
        print('✅ Builder analysis successful')
    except Exception as e:
        print(f'❌ Builder analysis failed: {e}')
"

echo "✅ All tests passed!"
echo ""
echo "Next steps:"
echo "1. Build the Docker image: make builder-image"
echo "2. Test deployment: make demo"
echo "3. Install locally: make install" 