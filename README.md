- 👋 Hi, I’m @Boujelajel
- 👀 I’m interested in ...
- 🌱 I’m currently learning ...
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me ...

<!---
Boujelajel/Boujelajel is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your #!/usr/bin/env python3
"""Create sample images for testing the montage creator"""
from PIL import Image, ImageDraw, ImageFont
import os
def create_sample_image(filename, color, text, size=(1920, 1080)):
    """Create a sample image with a solid color and text"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    # Try to use a larger font
    try:
