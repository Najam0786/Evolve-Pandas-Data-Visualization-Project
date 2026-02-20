import pandas as pd


def assert_columns(df: pd.DataFrame, required: list) -> None:
    """Raise ValueError if any required columns are missing from df."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def null_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary of null values per column (only columns with nulls)."""
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0].sort_values(ascending=False)
    pct = (nulls / len(df) * 100).round(1)
    return pd.DataFrame({"null_count": nulls, "null_pct": pct})


def assert_no_full_null_columns(df: pd.DataFrame) -> None:
    """Raise ValueError if any column is 100% null."""
    full_null = [c for c in df.columns if df[c].isnull().all()]
    if full_null:
        raise ValueError(f"Columns are entirely null: {full_null}")
