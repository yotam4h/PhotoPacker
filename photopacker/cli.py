"""
Command-line interface for PhotoPacker.
"""

import argparse
import logging
import sys
from typing import List, Optional

from .constants import DEFAULT_DPI, DEFAULT_MARGIN_MM, DEFAULT_PAGE_SIZE, PAGE_SIZES
from .core import PhotoPacker

# Set up logger
logger = logging.getLogger(__name__)

def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: Whether to enable debug logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(levelname)s: %(message)s'
    
    if verbose:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="PhotoPacker - Create photo collages with exact physical dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i input -o output
  %(prog)s -i input -o output --page-size a3
  %(prog)s -i input -o output --page-size a4 --margin 5
  %(prog)s -i input -o output --dpi 150

Input directory structure should contain size-named folders:
  input/
    10_10/     (for 10×10cm images)
    10_15/     (for 10×15cm images)
    13_18/     (for 13×18cm images)
    20_25/     (for 20×25cm images)
    ...

Supported page sizes: a4, a3, letter, legal
        """
    )
    
    parser.add_argument(
        '-i', '--input', 
        required=True,
        help='Input directory containing size-named folders'
    )
    parser.add_argument(
        '-o', '--output', 
        required=True,
        help='Output directory for collages'
    )
    parser.add_argument(
        '--page-size', 
        choices=list(PAGE_SIZES.keys()),
        default=DEFAULT_PAGE_SIZE, 
        help=f'Page size (default: {DEFAULT_PAGE_SIZE})'
    )
    parser.add_argument(
        '--dpi', 
        type=int, 
        default=DEFAULT_DPI,
        help=f'Output resolution in DPI (default: {DEFAULT_DPI})'
    )
    parser.add_argument(
        '--margin', 
        type=int, 
        default=DEFAULT_MARGIN_MM,
        help=f'Margin between images in millimeters (default: {DEFAULT_MARGIN_MM}mm)'
    )
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args(args)

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parsed_args = parse_args(args)
    
    # Set up logging
    setup_logging(parsed_args.verbose)
    
    # Create PhotoPacker instance
    packer = PhotoPacker(
        input_dir=parsed_args.input,
        output_dir=parsed_args.output,
        page_size=parsed_args.page_size,
        dpi=parsed_args.dpi,
        margin_mm=parsed_args.margin
    )
    
    # Process images
    return packer.process()