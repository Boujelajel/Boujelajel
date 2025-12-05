#!/bin/bash
# Simple wrapper script for creating video montages

echo "🎬 Video Montage Creator"
echo "========================"
echo ""

# Check if images provided
if [ $# -eq 0 ]; then
    echo "Usage: ./make_montage.sh <image_files>"
    echo ""
    echo "Examples:"
    echo "  ./make_montage.sh *.jpg"
    echo "  ./make_montage.sh my_images/*.jpg"
    echo "  ./make_montage.sh photo1.jpg photo2.jpg photo3.jpg"
    echo ""
    echo "For more options, use:"
    echo "  python3 create_montage.py --help"
    exit 1
fi

# Count images
image_count=$#
echo "Found $image_count images"
echo ""

# Ask for style
echo "Choose style:"
echo "  1) Simple crossfade (fast, recommended)"
echo "  2) Ken Burns effect (slow, dynamic pan/zoom)"
read -p "Enter choice [1]: " style_choice
style_choice=${style_choice:-1}

if [ "$style_choice" = "2" ]; then
    style="kenburns"
    echo "✓ Using Ken Burns effect"
else
    style="simple"
    echo "✓ Using simple crossfade"
fi
echo ""

# Ask for duration
read -p "Duration per image in seconds [3]: " duration
duration=${duration:-3}
echo "✓ Duration: ${duration}s per image"
echo ""

# Ask for output name
read -p "Output filename [montage.mp4]: " output
output=${output:-montage.mp4}
echo "✓ Output: $output"
echo ""

# Build command
cmd="python3 create_montage.py"
for img in "$@"; do
    cmd="$cmd \"$img\""
done
cmd="$cmd --output \"$output\" --duration $duration --style $style"

echo "Creating your montage..."
echo ""

# Execute
eval $cmd

echo ""
echo "Done! Your video is ready: $output"
