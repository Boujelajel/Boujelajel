#!/usr/bin/env python3
"""
Video Montage Creator
Creates professional video montages from images with transitions and effects
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from PIL import Image
import argparse


class VideoMontageCreator:
    def __init__(self, output_file="montage.mp4", duration_per_image=3, 
                 transition_duration=1, resolution="1920x1080", fps=30):
        self.output_file = output_file
        self.duration_per_image = duration_per_image
        self.transition_duration = transition_duration
        self.resolution = resolution
        self.fps = fps
        self.width, self.height = map(int, resolution.split('x'))
        
    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def prepare_images(self, image_paths, temp_dir="temp_processed"):
        """Prepare and resize images to consistent dimensions"""
        Path(temp_dir).mkdir(exist_ok=True)
        processed_images = []
        
        print(f"Processing {len(image_paths)} images...")
        
        for idx, img_path in enumerate(image_paths):
            try:
                img = Image.open(img_path)
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate aspect ratio preserving resize
                img_ratio = img.width / img.height
                target_ratio = self.width / self.height
                
                if img_ratio > target_ratio:
                    # Image is wider, fit to height
                    new_height = self.height
                    new_width = int(new_height * img_ratio)
                else:
                    # Image is taller, fit to width
                    new_width = self.width
                    new_height = int(new_width / img_ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create canvas and center image
                canvas = Image.new('RGB', (self.width, self.height), (0, 0, 0))
                x_offset = (self.width - new_width) // 2
                y_offset = (self.height - new_height) // 2
                canvas.paste(img, (x_offset, y_offset))
                
                output_path = os.path.join(temp_dir, f"img_{idx:04d}.jpg")
                canvas.save(output_path, 'JPEG', quality=95)
                processed_images.append(output_path)
                
                print(f"  ✓ Processed: {os.path.basename(img_path)}")
                
            except Exception as e:
                print(f"  ✗ Error processing {img_path}: {e}")
                continue
        
        return processed_images
    
    def create_montage_simple(self, image_paths, audio_path=None):
        """Create a simple montage with crossfade transitions"""
        if not self.check_ffmpeg():
            print("Error: FFmpeg is not installed!")
            return False
        
        processed_images = self.prepare_images(image_paths)
        
        if len(processed_images) < 2:
            print("Error: Need at least 2 images for a montage")
            return False
        
        print(f"\nCreating video montage with {len(processed_images)} images...")
        
        # Build FFmpeg filter complex for crossfade transitions
        filter_parts = []
        
        # Calculate timing
        total_duration = (self.duration_per_image * len(processed_images)) - \
                        (self.transition_duration * (len(processed_images) - 1))
        
        # Input all images
        inputs = []
        for img in processed_images:
            inputs.extend(['-loop', '1', '-t', str(self.duration_per_image), '-i', img])
        
        # Build crossfade filter chain
        current_stream = '[0:v]'
        for i in range(1, len(processed_images)):
            offset = (self.duration_per_image * i) - (self.transition_duration * i)
            next_stream = f'[v{i}]' if i < len(processed_images) - 1 else '[outv]'
            
            filter_parts.append(
                f"{current_stream}[{i}:v]xfade=transition=fade:"
                f"duration={self.transition_duration}:"
                f"offset={offset - self.transition_duration}{next_stream}"
            )
            current_stream = next_stream
        
        filter_complex = ';'.join(filter_parts)
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-y'] + inputs
        cmd.extend([
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-r', str(self.fps)
        ])
        
        # Add audio if provided
        if audio_path and os.path.exists(audio_path):
            cmd.extend([
                '-i', audio_path,
                '-map', '0:a?',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest'
            ])
        
        cmd.append(self.output_file)
        
        print(f"\nRendering video...")
        print(f"Command: {' '.join(cmd[:10])}... (truncated)")
        
        try:
            result = subprocess.run(cmd, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            if result.returncode == 0:
                print(f"\n✓ Video created successfully: {self.output_file}")
                file_size = os.path.getsize(self.output_file) / (1024 * 1024)
                print(f"  File size: {file_size:.2f} MB")
                print(f"  Duration: ~{total_duration:.1f} seconds")
                return True
            else:
                print(f"\n✗ FFmpeg error:")
                print(result.stderr[-500:])  # Last 500 chars of error
                return False
                
        except Exception as e:
            print(f"\n✗ Error running FFmpeg: {e}")
            return False
    
    def create_montage_kenburns(self, image_paths, audio_path=None):
        """Create montage with Ken Burns effect (pan and zoom)"""
        if not self.check_ffmpeg():
            print("Error: FFmpeg is not installed!")
            return False
        
        processed_images = self.prepare_images(image_paths)
        
        if len(processed_images) < 1:
            print("Error: Need at least 1 image")
            return False
        
        print(f"\nCreating Ken Burns style montage with {len(processed_images)} images...")
        
        # Build FFmpeg command with zoompan filter
        inputs = []
        filter_parts = []
        
        for idx, img in enumerate(processed_images):
            inputs.extend(['-loop', '1', '-t', str(self.duration_per_image), '-i', img])
            
            # Alternate between zoom in and zoom out
            zoom_direction = 'in' if idx % 2 == 0 else 'out'
            
            if zoom_direction == 'in':
                zoom_expr = f"'if(lte(zoom,1.3),zoom+0.002,1.3)'"
            else:
                zoom_expr = f"'if(gte(zoom,1.0),zoom-0.002,1.0)'"
            
            filter_parts.append(
                f"[{idx}:v]zoompan=z={zoom_expr}:"
                f"d={self.duration_per_image * self.fps}:"
                f"s={self.width}x{self.height}:"
                f"fps={self.fps}[v{idx}]"
            )
        
        # Concatenate all clips
        concat_inputs = ''.join([f'[v{i}]' for i in range(len(processed_images))])
        filter_parts.append(f"{concat_inputs}concat=n={len(processed_images)}:v=1:a=0[outv]")
        
        filter_complex = ';'.join(filter_parts)
        
        cmd = ['ffmpeg', '-y'] + inputs
        cmd.extend([
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-pix_fmt', 'yuv420p'
        ])
        
        if audio_path and os.path.exists(audio_path):
            cmd.extend([
                '-i', audio_path,
                '-map', '0:a?',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest'
            ])
        
        cmd.append(self.output_file)
        
        print(f"\nRendering video with Ken Burns effect...")
        
        try:
            result = subprocess.run(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            if result.returncode == 0:
                print(f"\n✓ Video created successfully: {self.output_file}")
                file_size = os.path.getsize(self.output_file) / (1024 * 1024)
                print(f"  File size: {file_size:.2f} MB")
                return True
            else:
                print(f"\n✗ FFmpeg error:")
                print(result.stderr[-500:])
                return False
                
        except Exception as e:
            print(f"\n✗ Error running FFmpeg: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Create professional video montages from images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple crossfade montage
  python create_montage.py image1.jpg image2.jpg image3.jpg
  
  # Ken Burns effect with custom duration
  python create_montage.py *.jpg --style kenburns --duration 4
  
  # Add background music
  python create_montage.py *.jpg --audio music.mp3
  
  # Custom resolution for Instagram
  python create_montage.py *.jpg --resolution 1080x1080
        """
    )
    
    parser.add_argument('images', nargs='+', help='Input image files')
    parser.add_argument('-o', '--output', default='montage.mp4', 
                       help='Output video file (default: montage.mp4)')
    parser.add_argument('-d', '--duration', type=float, default=3.0,
                       help='Duration per image in seconds (default: 3)')
    parser.add_argument('-t', '--transition', type=float, default=1.0,
                       help='Transition duration in seconds (default: 1)')
    parser.add_argument('-r', '--resolution', default='1920x1080',
                       help='Video resolution (default: 1920x1080)')
    parser.add_argument('-f', '--fps', type=int, default=30,
                       help='Frames per second (default: 30)')
    parser.add_argument('-a', '--audio', help='Background audio file')
    parser.add_argument('-s', '--style', choices=['simple', 'kenburns'], 
                       default='simple',
                       help='Montage style (default: simple)')
    
    args = parser.parse_args()
    
    # Validate images exist
    valid_images = []
    for img_path in args.images:
        if os.path.exists(img_path):
            valid_images.append(img_path)
        else:
            print(f"Warning: Image not found: {img_path}")
    
    if not valid_images:
        print("Error: No valid images found!")
        return 1
    
    print(f"Video Montage Creator")
    print(f"=" * 50)
    print(f"Images: {len(valid_images)}")
    print(f"Style: {args.style}")
    print(f"Resolution: {args.resolution}")
    print(f"Duration per image: {args.duration}s")
    if args.style == 'simple':
        print(f"Transition: {args.transition}s")
    print(f"=" * 50)
    
    creator = VideoMontageCreator(
        output_file=args.output,
        duration_per_image=args.duration,
        transition_duration=args.transition,
        resolution=args.resolution,
        fps=args.fps
    )
    
    if args.style == 'kenburns':
        success = creator.create_montage_kenburns(valid_images, args.audio)
    else:
        success = creator.create_montage_simple(valid_images, args.audio)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
