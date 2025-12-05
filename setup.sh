#!/bin/bash
# Setup script for Video Montage Creator

echo "Setting up Video Montage Creator..."
echo "===================================="

# Install FFmpeg
echo "Installing FFmpeg..."
sudo dnf install -y ffmpeg

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install Pillow

echo ""
echo "✓ Setup complete!"
echo ""
echo "Usage:"
echo "  python3 create_montage.py image1.jpg image2.jpg image3.jpg"
echo ""
echo "For more options:"
echo "  python3 create_montage.py --help"
