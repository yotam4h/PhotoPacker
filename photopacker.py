#!/usr/bin/env python3
"""
Wrapper script for backward compatibility with the old single-file version.
"""

import sys
from photopacker.cli import main

if __name__ == "__main__":
    sys.exit(main())
