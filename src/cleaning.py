import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline for the LinkedIn dataset.

    Note on remaining nulls after cleaning:
        This pipeline removes broken data (junk columns, corrupted values,
        duplicates) but intentionally preserves legitimate nulls:
        - endDate (22.5% null) — NaT means the person is still in that role.
        - genderEstimate (10.1%) — algorithm could not classify these profiles;
          imputing gender would introduce bias.
        - posLocation (28.2%) — not recorded in the original scrape.
        - companyStaffCount / companyFollowerCount (~3%) — not available for
          all companies.
        Dropping all rows with any null would discard a large portion of the
        dataset for no analytical benefit. Downstream functions apply dropna
        only on the specific columns they need.
    """
    out = df.copy()

    # 1. Drop unnamed / junk columns
    unnamed = [c for c in out.columns if "Unnamed" in str(c)]
    out = out.drop(columns=unnamed)

    # 2. Drop columns not useful for analysis (URLs, URNs, IDs, image flags)
    drop_cols = ["companyUrl", "companyUrn", "memberUrn", "positionId",
                 "companyHasLogo", "hasPicture", "followable", "followersCount",
                 "posLocationCode", "mbrLocationCode"]
    out = out.drop(columns=[c for c in drop_cols if c in out.columns])

    # 3. Standardise column names (strip whitespace)
    out.columns = [c.strip() for c in out.columns]

    # 4. Fix country — almost all rows are Australian; corrupt entries → 'au'
    if "country" in out.columns:
        out["country"] = out["country"].where(
            out["country"].isin(["au"]), other="au"
        )

    # 5. Fix genderEstimate — keep only 'male' / 'female', rest → NaN
    if "genderEstimate" in out.columns:
        valid_genders = ["male", "female"]
        out["genderEstimate"] = out["genderEstimate"].where(
            out["genderEstimate"].isin(valid_genders)
        )

    # 6. Fix isPremium — keep only '0' / '1', convert to int
    if "isPremium" in out.columns:
        out["isPremium"] = pd.to_numeric(out["isPremium"], errors="coerce")
        out["isPremium"] = out["isPremium"].where(
            out["isPremium"].isin([0, 1])
        ).fillna(0).astype(int)

    # 7. Convert numeric columns stored as text
    for col in ["connectionsCount", "companyStaffCount", "companyFollowerCount"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    # 8. Parse dates
    for col in ["startDate", "endDate"]:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")

    # 9. Strip whitespace from text columns
    text_cols = out.select_dtypes(include="object").columns
    for col in text_cols:
        out[col] = out[col].str.strip()

    # 10. Drop exact duplicate rows
    n_before = len(out)
    out = out.drop_duplicates()
    n_after = len(out)
    print(f"Cleaning: {n_before} → {n_after} rows ({n_before - n_after} duplicates removed)")

    return out
