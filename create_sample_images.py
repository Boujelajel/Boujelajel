#!/usr/bin/env python3
"""Create sample images for testing the montage creator"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image(filename, color, text, size=(1920, 1080)):
    """Create a sample image with a solid color and text"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font
    try:
        font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw text with shadow
    shadow_offset = 5
    draw.text((position[0] + shadow_offset, position[1] + shadow_offset), 
              text, fill=(0, 0, 0), font=font)
    draw.text(position, text, fill=(255, 255, 255), font=font)
    
    # Add some decorative elements
    draw.rectangle([50, 50, size[0]-50, size[1]-50], outline=(255, 255, 255), width=10)
    
    img.save(filename, 'JPEG', quality=95)
    print(f"Created: {filename}")

# Create sample images
os.makedirs('sample_images', exist_ok=True)

samples = [
    ('sample_images/image1.jpg', (41, 128, 185), 'Scene 1'),   # Blue
    ('sample_images/image2.jpg', (231, 76, 60), 'Scene 2'),    # Red
    ('sample_images/image3.jpg', (46, 204, 113), 'Scene 3'),   # Green
    ('sample_images/image4.jpg', (241, 196, 15), 'Scene 4'),   # Yellow
    ('sample_images/image5.jpg', (155, 89, 182), 'Scene 5'),   # Purple
]

for filename, color, text in samples:
    create_sample_image(filename, color, text)

print(f"\n✓ Created {len(samples)} sample images in 'sample_images/' directory")
