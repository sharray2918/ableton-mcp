#!/bin/bash
set -e

echo "🚀 Setting up Fairway Buddies AI Prompt Generation Workflow..."

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is not installed. Please install it first:"
    echo "   npm install -g pnpm"
    echo "   or visit: https://pnpm.io/installation"
    exit 1
fi

# Check if repomix is available globally (optional)
if command -v repomix &> /dev/null; then
    echo "✅ repomix found globally"
    REPOMIX_VERSION=$(repomix --version 2>/dev/null || echo "unknown")
    echo "   Version: $REPOMIX_VERSION"
else
    echo "ℹ️  repomix not found globally - will install locally"
fi

# Navigate to scripts directory
cd "$(dirname "$0")"
echo "📁 Working directory: $(pwd)"

# Install dependencies
echo "📦 Installing dependencies with pnpm..."
pnpm install

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x ./scripts/generate.js
chmod +x ./scripts/cleanup.js

# Create generated directory if it doesn't exist
echo "📁 Creating generated directory..."
mkdir -p ./generated

# Test generation (dry run)
echo "🧪 Testing generation (dry run)..."
node scripts/generate.js --dry-run

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📚 Quick start:"
echo "   pnpm run generate          # Generate repository XML"
echo "   pnpm run cleanup           # Clean up old files"
echo "   pnpm run generate list     # List generated files"
echo ""
echo "📖 See README.md for detailed usage instructions"
echo "📝 Check templates/prompt-template.md for AI prompt examples"
