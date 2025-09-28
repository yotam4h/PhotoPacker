"""
Entry point for running the package as a module.
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())