"""
paths.py

Centralized project paths for the
N100 Financial Intelligence Platform.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data folders
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SUPPORTING_DATA_DIR = PROJECT_ROOT / "data" / "supporting"

# Database folder
DATABASE_DIR = PROJECT_ROOT / "db"

# Output folders
OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"