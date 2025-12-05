# Video Montage Creator

Create professional video montages from your images with smooth transitions and effects.

## Features

- **Multiple Transition Styles**: Crossfade transitions or Ken Burns effect (pan & zoom)
- **Customizable Duration**: Set how long each image displays
- **Background Music**: Add audio tracks to your montage
- **Multiple Resolutions**: Support for YouTube (1920x1080), Instagram (1080x1080), TikTok (1080x1920)
- **High Quality Output**: H.264 encoded MP4 files optimized for social media

## Quick Start

### 1. Setup (First Time Only)

```bash
chmod +x setup.sh
./setup.sh
```

### 2. Create Your Montage

**Simple crossfade montage:**
```bash
python3 create_montage.py image1.jpg image2.jpg image3.jpg
```

**Ken Burns effect (pan and zoom):**
```bash
python3 create_montage.py *.jpg --style kenburns
```

**With background music:**
```bash
python3 create_montage.py *.jpg --audio music.mp3
```

**Custom settings:**
```bash
python3 create_montage.py *.jpg \
  --output my_video.mp4 \
  --duration 4 \
  --transition 1.5 \
  --resolution 1920x1080 \
  --fps 30
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output video filename | `montage.mp4` |
| `-d, --duration` | Duration per image (seconds) | `3` |
| `-t, --transition` | Transition duration (seconds) | `1` |
| `-r, --resolution` | Video resolution (WxH) | `1920x1080` |
| `-f, --fps` | Frames per second | `30` |
| `-a, --audio` | Background audio file | None |
| `-s, --style` | Style: `simple` or `kenburns` | `simple` |

## Common Resolutions

- **YouTube/Landscape**: `1920x1080` (16:9)
- **Instagram Square**: `1080x1080` (1:1)
- **Instagram Story/TikTok**: `1080x1920` (9:16)
- **4K**: `3840x2160` (16:9)

## Examples

### Travel Montage
```bash
python3 create_montage.py \
  vacation1.jpg vacation2.jpg vacation3.jpg \
  --style kenburns \
  --duration 4 \
  --audio travel_music.mp3 \
  --output travel_montage.mp4
```

### Instagram Post
```bash
python3 create_montage.py *.jpg \
  --resolution 1080x1080 \
  --duration 2.5 \
  --output instagram_post.mp4
```

### YouTube Intro
```bash
python3 create_montage.py intro_*.jpg \
  --resolution 1920x1080 \
  --duration 3 \
  --transition 0.5 \
  --fps 60 \
  --output youtube_intro.mp4
```

## Tips

1. **Image Order**: Images are processed in the order you specify. Use wildcards (`*.jpg`) for alphabetical order.

2. **Image Quality**: Use high-resolution images (at least 1920x1080) for best results.

3. **Audio Length**: If audio is shorter than the video, it will loop. If longer, video will end when images finish.

4. **Performance**: Ken Burns effect takes longer to render than simple crossfade.

5. **File Formats**: Supports JPG, JPEG, PNG images. Output is always MP4 (H.264).

## Troubleshooting

**FFmpeg not found:**
```bash
sudo dnf install -y ffmpeg
```

**Pillow not installed:**
```bash
pip3 install Pillow
```

**Out of memory:**
- Reduce resolution
- Process fewer images at once
- Use simple style instead of kenburns

## Technical Details

- **Video Codec**: H.264 (libx264)
- **Audio Codec**: AAC
- **Pixel Format**: yuv420p (maximum compatibility)
- **Preset**: medium (balance between speed and quality)
- **CRF**: 23 (high quality)

## License

Free to use for personal and commercial projects.
