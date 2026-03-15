"""
Test configuration and utilities
"""
import pytest
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Test data directory
TEST_DATA_DIR = PROJECT_ROOT / 'datasets'

# Model directory
MODEL_DIR = PROJECT_ROOT / 'models'
