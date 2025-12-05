# Quick Start Guide - Video Montage Creator

## ✅ Setup Complete!

Your video montage creator is ready to use. All dependencies are installed:
- ✓ Python 3 with Pillow
- ✓ FFmpeg 7.0.2

## 🎬 Create Your First Montage

### Step 1: Prepare Your Images

Place your images in a folder. Supported formats: JPG, JPEG, PNG

```bash
# Example: Create a folder for your images
mkdir my_images
# Copy your images there
cp /path/to/your/images/*.jpg my_images/
```

### Step 2: Create the Montage

**Simple crossfade montage (recommended for beginners):**
```bash
python3 create_montage.py my_images/*.jpg
```

This creates `montage.mp4` with:
- 3 seconds per image
- 1 second crossfade transitions
- 1920x1080 resolution (Full HD)

### Step 3: Customize (Optional)

**Change duration and output name:**
```bash
python3 create_montage.py my_images/*.jpg \
  --output my_video.mp4 \
  --duration 4 \
  --transition 1.5
```

**Ken Burns effect (pan and zoom):**
```bash
python3 create_montage.py my_images/*.jpg \
  --style kenburns \
  --duration 4
```

**Add background music:**
```bash
python3 create_montage.py my_images/*.jpg \
  --audio background_music.mp3
```

**Instagram square format:**
```bash
python3 create_montage.py my_images/*.jpg \
  --resolution 1080x1080
```

**TikTok/Instagram Story (vertical):**
```bash
python3 create_montage.py my_images/*.jpg \
  --resolution 1080x1920
```

## 📱 Common Use Cases

### Travel Video
```bash
python3 create_montage.py vacation_photos/*.jpg \
  --style kenburns \
  --duration 4 \
  --audio travel_music.mp3 \
  --output travel_memories.mp4
```

### Quick Social Media Post
```bash
python3 create_montage.py photos/*.jpg \
  --duration 2 \
  --transition 0.5 \
  --resolution 1080x1080 \
  --output instagram.mp4
```

### YouTube Channel Intro
```bash
python3 create_montage.py intro_images/*.jpg \
  --duration 2.5 \
  --fps 60 \
  --output youtube_intro.mp4
```

## 🎨 Demo Videos

Two demo videos have been created for you:

1. **demo_simple.mp4** - Crossfade transitions (108 KB, 7.5 seconds)
2. **demo_kenburns.mp4** - Ken Burns pan/zoom effect (7.3 MB)

View them to see the different styles!

## 📋 All Options

```
-o, --output FILE       Output filename (default: montage.mp4)
-d, --duration SECONDS  Duration per image (default: 3)
-t, --transition SEC    Transition duration (default: 1)
-r, --resolution WxH    Video resolution (default: 1920x1080)
-f, --fps NUMBER        Frames per second (default: 30)
-a, --audio FILE        Background audio file
-s, --style TYPE        Style: simple or kenburns (default: simple)
```

## 💡 Tips

1. **Image Order**: Images are processed alphabetically. Rename them if you need a specific order:
   ```bash
   # Rename to control order
   mv photo1.jpg 01_photo.jpg
   mv photo2.jpg 02_photo.jpg
   ```

2. **High Quality**: Use high-resolution images (at least 1920x1080) for best results

3. **Performance**: 
   - Simple style renders faster
   - Ken Burns effect takes longer but looks more dynamic
   - Lower resolution = faster rendering

4. **Audio**: 
   - MP3, WAV, AAC formats supported
   - Audio will loop if shorter than video
   - Video ends when images finish (not when audio ends)

## 🆘 Need Help?

View all options:
```bash
python3 create_montage.py --help
```

## 🎯 Your Images

To use YOUR uploaded images, you'll need to:

1. Save them to the filesystem first
2. Then run the montage creator on them

Example:
```bash
# If your images are in /vercel/sandbox/uploads/
python3 create_montage.py /vercel/sandbox/uploads/*.jpg --output my_montage.mp4
```

---

**Ready to create amazing video montages! 🎥✨**
