"""
Tests for the CLI module.
"""

import unittest
from unittest import mock
import argparse
import sys
from photopacker.cli import parse_args, main

class TestCLI(unittest.TestCase):
    """Test case for CLI functionality."""

    def test_parse_args_default_values(self):
        """Test that default values are set correctly when parsing args."""
        args = parse_args(["-i", "input", "-o", "output"])
        
        self.assertEqual(args.input, "input")
        self.assertEqual(args.output, "output")
        self.assertEqual(args.page_size, "a4")
        self.assertEqual(args.dpi, 300)
        self.assertEqual(args.margin, 2)
        self.assertFalse(args.verbose)
        
    def test_parse_args_custom_values(self):
        """Test that custom values are parsed correctly."""
        args = parse_args([
            "-i", "custom_input", 
            "-o", "custom_output", 
            "--page-size", "a3",
            "--dpi", "150",
            "--margin", "5",
            "--verbose"
        ])
        
        self.assertEqual(args.input, "custom_input")
        self.assertEqual(args.output, "custom_output")
        self.assertEqual(args.page_size, "a3")
        self.assertEqual(args.dpi, 150)
        self.assertEqual(args.margin, 5)
        self.assertTrue(args.verbose)
        
    @mock.patch("photopacker.cli.PhotoPacker")
    def test_main_creates_photopacker_instance(self, mock_packer_class):
        """Test that main creates a PhotoPacker instance with the right args."""
        # Setup mock
        mock_packer_instance = mock_packer_class.return_value
        mock_packer_instance.process.return_value = 0
        
        # Call main with test args
        result = main(["-i", "input", "-o", "output", "--page-size", "a3"])
        
        # Assert PhotoPacker was created with the right args
        mock_packer_class.assert_called_once_with(
            input_dir="input",
            output_dir="output",
            page_size="a3",
            dpi=300,
            margin_mm=2
        )
        
        # Assert process was called and return value is correct
        mock_packer_instance.process.assert_called_once()
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()