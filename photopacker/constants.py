"""
Constants and configuration values used throughout the PhotoPacker package.
"""

# Page sizes in centimeters (width, height)
PAGE_SIZES = {
    'a4': (21.0, 29.7),
    'a3': (29.7, 42.0),
    'letter': (21.6, 27.9),
    'legal': (21.6, 35.6)
}

# Default settings
DEFAULT_DPI = 300  # Standard print quality
DEFAULT_MARGIN_MM = 2  # Default margin in millimeters
DEFAULT_PAGE_SIZE = 'a4'  # Default page size

# Image file extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp'}