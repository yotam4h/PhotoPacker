#!/usr/bin/env bash
# Simple installation script for PhotoPacker

echo "Installing PhotoPacker..."

# Install package in development mode
pip install -e .

echo "Installation complete!"
echo ""
echo "You can now use PhotoPacker with:"
echo "  photopacker -i input_directory -o output_directory"
echo ""
echo "Or by running the module:"
echo "  python -m photopacker -i input_directory -o output_directory"