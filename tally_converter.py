#!/usr/bin/env python3
"""
Tally XML Converter - Main Entry Point
Converts SBI bank statement PDFs to Tally-compatible XML format.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from converter import main

if __name__ == "__main__":
    main()
