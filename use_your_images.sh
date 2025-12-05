#!/bin/bash
# Helper script to use your uploaded images

echo "🖼️  Using Your Uploaded Images"
echo "================================"
echo ""

# Check if uploads directory exists
if [ ! -d "uploads" ]; then
    echo "Creating 'uploads' directory..."
    mkdir -p uploads
    echo "✓ Directory created"
    echo ""
fi

# Check for images
image_count=$(find uploads -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) 2>/dev/null | wc -l)

if [ $image_count -eq 0 ]; then
    echo "⚠️  No images found in 'uploads/' directory"
    echo ""
    echo "To use your images:"
    echo "  1. Copy your images to the 'uploads/' folder"
    echo "  2. Run this script again"
    echo ""
    echo "Example:"
    echo "  cp /path/to/your/images/*.jpg uploads/"
    echo "  ./use_your_images.sh"
    echo ""
    echo "Or use the montage creator directly:"
    echo "  python3 create_montage.py /path/to/your/images/*.jpg"
    exit 1
fi

echo "✓ Found $image_count images in uploads/"
echo ""

# List images
echo "Images found:"
find uploads -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | sort | head -10
if [ $image_count -gt 10 ]; then
    echo "... and $((image_count - 10)) more"
fi
echo ""

# Ask to proceed
read -p "Create montage from these images? [Y/n]: " proceed
proceed=${proceed:-Y}

if [[ ! $proceed =~ ^[Yy] ]]; then
    echo "Cancelled."
    exit 0
fi

# Run the interactive script
./make_montage.sh uploads/*.{jpg,jpeg,png,JPG,JPEG,PNG} 2>/dev/null
