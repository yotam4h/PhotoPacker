#!/usr/bin/env python3
"""
Setup script for PhotoPacker.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read version from package __init__.py
about = {}
with open(os.path.join("photopacker", "__init__.py"), encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="photopacker",
    version=about["__version__"],
    description="A tool for creating photo collages with exact physical dimensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yotam",
    url="https://github.com/yotam4h/PhotoPacker",
    packages=find_packages(),
    install_requires=["Pillow>=9.0.0"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "photopacker=photopacker.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
    ],
)