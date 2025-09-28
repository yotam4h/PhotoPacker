"""
Core functionality for the PhotoPacker package.
"""

import os
import logging
from typing import Dict, List, Tuple
from pathlib import Path
from PIL import Image

from .constants import PAGE_SIZES, IMAGE_EXTENSIONS
from .image_utils import cm_to_pixels, resize_image_to_fit, center_on_background

# Set up logger
logger = logging.getLogger(__name__)

class PhotoPacker:
    """Handles photo processing and collage creation with exact physical dimensions."""
    
    def __init__(
        self, 
        input_dir: str, 
        output_dir: str, 
        page_size: str = 'a4', 
        dpi: int = 300, 
        margin_mm: int = 2
    ):
        """
        Initialize PhotoPacker.
        
        Args:
            input_dir: Directory containing size-named folders with images
            output_dir: Directory for output files
            page_size: Page size ('a4', 'a3', 'letter', 'legal')
            dpi: Resolution for output images (default: 300 for photo printing)
            margin_mm: Margin between images in millimeters (default: 2mm)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.page_size = page_size.lower()
        self.dpi = dpi
        self.margin_mm = margin_mm
        
        # Validate page size
        if self.page_size not in PAGE_SIZES:
            raise ValueError(f"Unsupported page size: {page_size}")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "collages").mkdir(exist_ok=True)
        
        logger.info(f"Initialized PhotoPacker with: input={self.input_dir}, "
                  f"output={self.output_dir}, page_size={self.page_size}, "
                  f"dpi={self.dpi}, margin={self.margin_mm}mm")

    def process(self) -> int:
        """
        Process all images in size-named directories and create direct collages.
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        logger.info("Starting photo processing (direct collage mode)")
        
        try:
            self._create_direct_collages()
            logger.info("Processing completed successfully!")
            return 0
        except Exception as e:
            logger.error(f"Error during processing: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return 1

    def _create_direct_collages(self) -> None:
        """Create collages by placing images directly without individual processing."""
        logger.info("Creating direct collages...")
        
        # Get page dimensions
        page_width_cm, page_height_cm = PAGE_SIZES[self.page_size]
        margin_cm = self.margin_mm / 10.0  # Convert mm to cm
        
        # Group images by size
        size_groups = self._group_images_by_size()
        
        if not size_groups:
            logger.warning("No size-named folders found in input directory")
            return
        
        # Count for naming collages
        collage_count = 0
        
        # Process each size group
        for (image_width_cm, image_height_cm), image_paths in size_groups.items():
            # Calculate how many images can fit per page
            available_width = page_width_cm - 2 * margin_cm
            available_height = page_height_cm - 2 * margin_cm
            
            # Calculate grid dimensions
            cols = int((available_width + margin_cm) / (image_width_cm + margin_cm))
            rows = int((available_height + margin_cm) / (image_height_cm + margin_cm))
            
            images_per_page = cols * rows
            
            logger.info(f"Size {image_width_cm}×{image_height_cm}cm: "
                      f"{len(image_paths)} images, "
                      f"{cols}×{rows} grid ({images_per_page} per page)")
            
            if images_per_page == 0:
                logger.warning(f"Images {image_width_cm}×{image_height_cm}cm are too large "
                             f"for {self.page_size} pages")
                continue
            
            # Create collages for this size group
            for i in range(0, len(image_paths), images_per_page):
                batch_images = image_paths[i:i + images_per_page]
                collage_count += 1
                
                self._create_single_collage(
                    batch_images, collage_count, 
                    image_width_cm, image_height_cm,
                    cols, rows, margin_cm
                )

    def _group_images_by_size(self) -> Dict[Tuple[float, float], List[Path]]:
        """
        Group images by their intended size based on folder names.
        
        Returns:
            Dictionary mapping (width_cm, height_cm) to a list of image paths
        """
        size_groups = {}
        
        for folder in self.input_dir.iterdir():
            if not folder.is_dir():
                continue
            
            # Parse folder name (e.g., "10_15" for 10×15cm)
            try:
                parts = folder.name.split('_')
                if len(parts) == 2:
                    width_cm = float(parts[0])
                    height_cm = float(parts[1])
                    
                    # Get all images in this folder
                    images = [
                        f for f in folder.iterdir() 
                        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
                    ]
                    
                    if images:
                        size_groups[(width_cm, height_cm)] = images
                        logger.info(f"Found {len(images)} images for size {width_cm}×{height_cm}cm")
                        
            except ValueError:
                logger.warning(f"Skipping folder with invalid name format: {folder.name}")
                continue
        
        return size_groups

    def _create_single_collage(
        self, 
        image_paths: List[Path], 
        collage_number: int,
        image_width_cm: float, 
        image_height_cm: float,
        cols: int, 
        rows: int, 
        margin_cm: float
    ) -> None:
        """
        Create a single collage page.
        
        Args:
            image_paths: List of paths to images to include
            collage_number: Sequence number for this collage
            image_width_cm: Target image width in cm
            image_height_cm: Target image height in cm
            cols: Number of columns in grid
            rows: Number of rows in grid
            margin_cm: Margin between images in cm
        """
        # Get page dimensions in pixels
        page_width_cm, page_height_cm = PAGE_SIZES[self.page_size]
        page_width_px = cm_to_pixels(page_width_cm, self.dpi)
        page_height_px = cm_to_pixels(page_height_cm, self.dpi)
        
        # Convert measurements to pixels
        image_width_px = cm_to_pixels(image_width_cm, self.dpi)
        image_height_px = cm_to_pixels(image_height_cm, self.dpi)
        margin_px = cm_to_pixels(margin_cm, self.dpi)
        
        # Create white background
        collage = Image.new('RGB', (page_width_px, page_height_px), 'white')
        
        # Calculate starting position for centering the grid
        grid_width = cols * image_width_px + (cols - 1) * margin_px
        grid_height = rows * image_height_px + (rows - 1) * margin_px
        
        start_x = (page_width_px - grid_width) // 2
        start_y = (page_height_px - grid_height) // 2
        
        # Place images
        for idx, image_path in enumerate(image_paths):
            if idx >= cols * rows:  # Safety check
                break
                
            row = idx // cols
            col = idx % cols
            
            # Calculate position
            x = start_x + col * (image_width_px + margin_px)
            y = start_y + row * (image_height_px + margin_px)
            
            try:
                # Load image
                img = Image.open(image_path)
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to fit
                img_resized = resize_image_to_fit(img, image_width_px, image_height_px)
                
                # Center on white background
                img_centered = center_on_background(img_resized, image_width_px, image_height_px)
                
                # Paste onto collage
                collage.paste(img_centered, (x, y))
                
            except Exception as e:
                logger.error(f"Error processing image {image_path}: {e}")
                continue
        
        # Save collage
        collage_path = self.output_dir / "collages" / f"collage_{collage_number:03d}.png"
        collage.save(collage_path, 'PNG', dpi=(self.dpi, self.dpi))
        logger.info(f"Created collage: {collage_path}")