"""
Tests for the core PhotoPacker functionality.
"""

import unittest
from unittest import mock
import os
import tempfile
from pathlib import Path
from PIL import Image

from photopacker.core import PhotoPacker
from photopacker.constants import PAGE_SIZES

class TestPhotoPacker(unittest.TestCase):
    """Test case for PhotoPacker functionality."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create temporary directories for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_dir = Path(self.temp_dir.name) / "input"
        self.output_dir = Path(self.temp_dir.name) / "output"
        
        # Create input structure
        os.makedirs(self.input_dir)
        os.makedirs(self.output_dir)
        
    def tearDown(self):
        """Clean up after each test."""
        self.temp_dir.cleanup()
        
    @mock.patch("photopacker.core.logger")
    def test_init_validates_page_size(self, mock_logger):
        """Test that initialization validates page size."""
        # Valid page size
        packer = PhotoPacker(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir),
            page_size="a4"
        )
        self.assertEqual(packer.page_size, "a4")
        
        # Invalid page size
        with self.assertRaises(ValueError) as context:
            PhotoPacker(
                input_dir=str(self.input_dir),
                output_dir=str(self.output_dir),
                page_size="invalid"
            )
        self.assertIn("Unsupported page size", str(context.exception))
        
    def test_output_dir_creation(self):
        """Test that output directories are created."""
        # Remove output directory to test creation
        if self.output_dir.exists():
            import shutil
            shutil.rmtree(self.output_dir)
            
        packer = PhotoPacker(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )
        
        # Check that output directories were created
        self.assertTrue(self.output_dir.exists())
        self.assertTrue((self.output_dir / "collages").exists())
        
    @mock.patch("photopacker.core.logger")
    def test_group_images_by_size(self, mock_logger):
        """Test that images are correctly grouped by size folder."""
        # Create test folder structure
        folder_10_15 = self.input_dir / "10_15"
        folder_13_18 = self.input_dir / "13_18"
        os.makedirs(folder_10_15)
        os.makedirs(folder_13_18)
        
        # Create test images (empty files are sufficient for testing folder structure)
        (folder_10_15 / "image1.jpg").touch()
        (folder_10_15 / "image2.jpg").touch()
        (folder_13_18 / "image3.jpg").touch()
        
        # Create a non-image file to test filtering
        (folder_10_15 / "not_an_image.txt").touch()
        
        # Create an invalid folder to test error handling
        invalid_folder = self.input_dir / "invalid_folder"
        os.makedirs(invalid_folder)
        
        packer = PhotoPacker(
            input_dir=str(self.input_dir),
            output_dir=str(self.output_dir)
        )
        
        size_groups = packer._group_images_by_size()
        
        # Check that we have the expected groups
        self.assertEqual(len(size_groups), 2)
        self.assertTrue((10.0, 15.0) in size_groups)
        self.assertTrue((13.0, 18.0) in size_groups)
        
        # Check that the right number of images are in each group
        self.assertEqual(len(size_groups[(10.0, 15.0)]), 2)
        self.assertEqual(len(size_groups[(13.0, 18.0)]), 1)
        
        # Check that non-image files were filtered out
        self.assertFalse(any(p.name == "not_an_image.txt" for p in size_groups[(10.0, 15.0)]))

if __name__ == "__main__":
    unittest.main()