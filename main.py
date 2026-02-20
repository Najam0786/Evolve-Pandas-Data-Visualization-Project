from src.config import RAW_PATH, OUT_PATH
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.utils import assert_columns, assert_no_full_null_columns
from src.viz import (
    plot_age_distribution,
    plot_top_companies,
    plot_gender_by_age_group,
    plot_company_size_distribution,
    plot_tenure_by_age_group,
)


def main():
    # 1. Load
    df = load_csv(RAW_PATH)

    # 2. Clean
    df = clean(df)
    assert_no_full_null_columns(df)

    # 3. Features
    df = build_features(df)
    assert_columns(df, ["age_group", "company_size_category", "tenure_months"])

    # 4. Export
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved: {OUT_PATH}")

    # 5. Visualise
    plot_age_distribution(df)
    plot_top_companies(df)
    plot_gender_by_age_group(df)
    plot_company_size_distribution(df)
    plot_tenure_by_age_group(df)


if __name__ == "__main__":
    main()
