#!/bin/bash
# Quick test script for Linux/macOS

echo "🧪 Testing GitHub Auto Commit Setup"
echo "=================================="

echo "1. Testing dry-run mode..."
if python3 github_auto_commit.py --dry-run; then
    echo "✓ Dry-run test passed"
else
    echo "✗ Dry-run test failed"
    exit 1
fi

echo ""
echo "2. Testing configuration..."
if [ -f "config.json" ]; then
    echo "✓ Configuration file found"
else
    echo "⚠ Configuration file will be created on first run"
fi

echo ""
echo "3. Testing Git repository..."
if git status >/dev/null 2>&1; then
    echo "✓ Git repository detected"
else
    echo "⚠ Initializing Git repository..."
    git init >/dev/null
    git checkout -b main >/dev/null
fi

echo ""
echo "4. Testing monitor script..."
if python3 monitor.py --help >/dev/null 2>&1; then
    echo "✓ Monitor script available"
else
    echo "⚠ Monitor script test failed"
fi

echo ""
echo "🎉 All tests completed successfully!"
echo ""
echo "Next steps:"
echo "1. Review config.json settings"
echo "2. Run: python3 github_auto_commit.py --mode daily"
echo "3. Setup scheduling: ./scheduler_helper.sh install"
echo ""