#!/usr/bin/env python3
"""
Setup script for ECH0 Quantum Computing Module
Optional install for M4 Mac optimized quantum features

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
All Rights Reserved. PATENT PENDING.
"""

from setuptools import setup, find_packages
import sys

# Check Python version
if sys.version_info < (3, 9):
    sys.exit("ECH0 Quantum requires Python 3.9+")

# Read requirements
with open("requirements_quantum.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="ech0-quantum",
    version="1.0.0",
    author="Joshua Hendricks Cole",
    author_email="",
    description="M4 Mac Optimized Quantum Computing for ECH0, Oracle, and AIOS",
    long_description=open("README_QUANTUM.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/consciousness",
    packages=find_packages(where="ech0_modules"),
    package_dir={"": "ech0_modules"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=7.0", "pytest-cov>=4.0"],
        "gui": ["tkinter"],  # GUI support
    },
    entry_points={
        "console_scripts": [
            "ech0-quantum=quantum_api:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
