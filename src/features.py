import pandas as pd
import numpy as np


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create new features from the cleaned LinkedIn dataset."""
    out = df.copy()

    # Feature 1: age_group — categorise professionals by career stage
    if "ageEstimate" in out.columns:
        bins = [0, 30, 40, 50, 100]
        labels = ["20-30", "31-40", "41-50", "51+"]
        out["age_group"] = pd.cut(out["ageEstimate"], bins=bins, labels=labels)

    # Feature 2: company_size_category — small / medium / large
    if "companyStaffCount" in out.columns:
        out["company_size_category"] = pd.cut(
            out["companyStaffCount"],
            bins=[0, 100, 1000, 10000, np.inf],
            labels=["Small", "Medium", "Large", "Enterprise"],
        )

    # Feature 3: tenure_months — duration of each position
    if {"startDate", "endDate"}.issubset(out.columns):
        delta = out["endDate"] - out["startDate"]
        out["tenure_months"] = (delta.dt.days / 30.44).round(1)

    n_new = sum(c in out.columns for c in ["age_group", "company_size_category", "tenure_months"])
    print(f"Features: {n_new} new columns added")

    return out
