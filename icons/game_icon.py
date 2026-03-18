#!/usr/bin/env python3
"""
Game Icon Generator
Creates icon files for the stealth payload
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_game_icon():
    """Create a professional game icon"""
    # Create 256x256 icon
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background gradient (blue theme)
    for y in range(size):
        alpha = int(255 * (1 - y / size * 0.3))
        color = (30, 58, 138, alpha)  # Blue gradient
        draw.line([(0, y), (size, y)], fill=color)
    
    # Draw puzzle piece shape
    center_x, center_y = size // 2, size // 2
    piece_size = size // 3
    
    # Main puzzle piece body
    draw.rounded_rectangle(
        [center_x - piece_size, center_y - piece_size, 
         center_x + piece_size, center_y + piece_size],
        radius=20, fill=(251, 191, 36, 255), outline=(245, 158, 11, 255), width=4
    )
    
    # Puzzle piece tabs
    tab_size = piece_size // 3
    # Top tab
    draw.ellipse([center_x - tab_size//2, center_y - piece_size - tab_size//2,
                  center_x + tab_size//2, center_y - piece_size + tab_size//2],
                 fill=(251, 191, 36, 255), outline=(245, 158, 11, 255), width=2)
    
    # Right tab
    draw.ellipse([center_x + piece_size - tab_size//2, center_y - tab_size//2,
                  center_x + piece_size + tab_size//2, center_y + tab_size//2],
                 fill=(251, 191, 36, 255), outline=(245, 158, 11, 255), width=2)
    
    # Add "P" for Puzzle
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "P"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2
    
    # Text shadow
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 128))
    # Main text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
    
    return img

def save_icon_formats(img):
    """Save icon in multiple formats"""
    # Ensure icons directory exists
    os.makedirs('icons', exist_ok=True)
    
    # Save as PNG
    img.save('icons/game_icon.png', 'PNG')
    
    # Save as ICO (Windows icon)
    # Create multiple sizes for ICO
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icons = []
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    icons[0].save('icons/game_icon.ico', format='ICO', sizes=[(icon.width, icon.height) for icon in icons])
    
    print("Icons created successfully:")
    print("- icons/game_icon.png")
    print("- icons/game_icon.ico")

if __name__ == "__main__":
    icon = create_game_icon()
    save_icon_formats(icon)