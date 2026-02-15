#!/bin/bash
# Build documentation and package

set -e  # Exit on error

echo "Building documentation..."
uv run sphinx-build ./docs/source ./docs/build -a

echo "Building package..."
uv build

echo "✓ Documentation and package built successfully!"
