"""
Utility functions for image processing and manipulation.
"""

from PIL import Image
from typing import Tuple

def cm_to_pixels(cm: float, dpi: int) -> int:
    """
    Convert centimeters to pixels based on DPI.
    
    Args:
        cm: Size in centimeters
        dpi: Resolution in dots per inch
        
    Returns:
        Size in pixels
    """
    inches = cm / 2.54
    return int(inches * dpi)

def resize_image_to_fit(
    img: Image.Image, 
    target_width: int, 
    target_height: int
) -> Image.Image:
    """
    Resize an image to fit within target dimensions while maintaining aspect ratio.
    
    Args:
        img: The input image
        target_width: Target width in pixels
        target_height: Target height in pixels
        
    Returns:
        Resized image
    """
    # Calculate scaling to fit exactly in the target size while maintaining aspect ratio
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        # Image is wider, fit by width
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        # Image is taller, fit by height
        new_height = target_height
        new_width = int(target_height * img_ratio)
    
    # Resize image
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def center_on_background(
    img: Image.Image, 
    bg_width: int, 
    bg_height: int, 
    bg_color: Tuple[int, int, int] = (255, 255, 255)
) -> Image.Image:
    """
    Center an image on a background of specified size and color.
    
    Args:
        img: The input image
        bg_width: Background width in pixels
        bg_height: Background height in pixels
        bg_color: Background color as RGB tuple (default: white)
        
    Returns:
        New image centered on background
    """
    # Create white background for this image slot
    bg_img = Image.new('RGB', (bg_width, bg_height), bg_color)
    
    # Center the image on the background
    paste_x = (bg_width - img.width) // 2
    paste_y = (bg_height - img.height) // 2
    bg_img.paste(img, (paste_x, paste_y))
    
    return bg_img