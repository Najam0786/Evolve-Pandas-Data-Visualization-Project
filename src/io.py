from pathlib import Path
from typing import Union

import pandas as pd


def load_csv(path: Union[str, Path], encoding: str = "latin-1") -> pd.DataFrame:
    """Load a CSV file into a DataFrame with proper encoding."""
    df = pd.read_csv(path, encoding=encoding, low_memory=False)
    print(f"Loaded {path.name}: {df.shape[0]} rows × {df.shape[1]} columns")
    return df
