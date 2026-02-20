"""Project-wide path configuration."""

from pathlib import Path

# Root of the project (one level up from src/)
ROOT = Path(__file__).resolve().parent.parent

# Raw input data
RAW_PATH = ROOT / "data" / "raw" / "linkedin.csv"

# Cleaned output data
OUT_PATH = ROOT / "data" / "processed" / "linkedin_clean.csv"
