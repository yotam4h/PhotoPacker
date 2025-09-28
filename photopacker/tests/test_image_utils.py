"""
Tests for image utility functions.
"""

import unittest
from PIL import Image
import io

from photopacker.image_utils import cm_to_pixels, resize_image_to_fit, center_on_background

class TestImageUtils(unittest.TestCase):
    """Test case for image utility functions."""
    
    def test_cm_to_pixels(self):
        """Test conversion from cm to pixels."""
        # Test with standard 300 DPI
        self.assertEqual(cm_to_pixels(1.0, 300), 118)  # 1cm ≈ 0.3937 inches, 0.3937 * 300 = 118.11
        self.assertEqual(cm_to_pixels(2.54, 300), 300)  # 2.54cm = 1 inch, 1 * 300 = 300
        
        # Test with different DPI
        self.assertEqual(cm_to_pixels(2.54, 72), 72)  # 1 inch at 72 DPI = 72 pixels
        
    def test_resize_image_to_fit(self):
        """Test image resizing while maintaining aspect ratio."""
        # Create a test image
        img_width, img_height = 400, 200  # 2:1 aspect ratio
        img = Image.new('RGB', (img_width, img_height), color='red')
        
        # Test resize to fit in square (should be limited by height)
        resized = resize_image_to_fit(img, 300, 300)
        self.assertEqual(resized.height, 150)  # Height should be scaled down to 150
        self.assertEqual(resized.width, 300)   # Width should be scaled down to 300
        
        # Test resize to fit in portrait rectangle (should be limited by width)
        resized = resize_image_to_fit(img, 100, 300)
        self.assertEqual(resized.width, 100)   # Width should be scaled down to 100
        self.assertEqual(resized.height, 50)   # Height should be scaled down to 50
        
        # Test resize to fit in landscape rectangle (should be limited by height)
        resized = resize_image_to_fit(img, 500, 100)
        self.assertEqual(resized.height, 100)  # Height should be scaled down to 100
        self.assertEqual(resized.width, 200)   # Width should be scaled down to 200
        
    def test_center_on_background(self):
        """Test centering an image on a background."""
        # Create a test image
        img_width, img_height = 100, 100
        img = Image.new('RGB', (img_width, img_height), color='red')
        
        # Center on a larger background
        bg_width, bg_height = 300, 200
        centered = center_on_background(img, bg_width, bg_height)
        
        # Check dimensions
        self.assertEqual(centered.width, bg_width)
        self.assertEqual(centered.height, bg_height)
        
        # Check that the image is centered - test center pixel
        center_x = bg_width // 2
        center_y = bg_height // 2
        self.assertEqual(centered.getpixel((center_x, center_y)), (255, 0, 0))  # Red
        
        # Check corners - should be white
        self.assertEqual(centered.getpixel((0, 0)), (255, 255, 255))  # White
        self.assertEqual(centered.getpixel((bg_width-1, bg_height-1)), (255, 255, 255))  # White

if __name__ == "__main__":
    unittest.main()