# LinkedIn Profiles & Jobs — Exploratory Data Analysis

## Objective

Analyse **39,530 LinkedIn professional profiles** (snapshot from January 2018, Australia-focused) to uncover patterns in demographics, employment, and career tenure using Python, Pandas, and data visualisation best practices.

## Dataset

- **Source:** [LinkedIn Profiles and Jobs Dataset (Kaggle)](https://www.kaggle.com/datasets/)
- **File:** `data/raw/linkedin.csv` (16.6 MB, 39,530 rows × 41 columns)
- **Encoding:** `latin-1`
- **Licence:** CC0 — Public Domain

## Research Questions

1. What is the age and gender profile of LinkedIn professionals in Australia?
2. Which companies and company sizes dominate the professional landscape?
3. How does job tenure vary across career stages?

## Pipeline

```
data/raw/linkedin.csv
        │
        ▼
   src/io.py          →  load_csv() with latin-1 encoding
        │
        ▼
   src/cleaning.py    →  clean(): drop junk columns, fix corrupted values,
        │                 parse dates, convert dtypes, remove duplicates
        ▼
   src/features.py    →  build_features(): age_group, company_size_category,
        │                 tenure_months
        ▼
   src/viz.py         →  5 visualisation functions
        │
        ▼
   data/processed/linkedin_clean.csv   (cleaned output)
```

## Project Structure

```
├── data/
│   ├── raw/linkedin.csv            # Original dataset
│   └── processed/linkedin_clean.csv # Cleaned output
├── notebooks/
│   └── eda.ipynb                    # Full EDA notebook with narrative
├── src/
│   ├── __init__.py
│   ├── config.py                    # Path configuration
│   ├── io.py                        # load_csv()
│   ├── cleaning.py                  # clean() — 10-step pipeline
│   ├── features.py                  # build_features() — 3 new columns
│   ├── viz.py                       # 5 plot functions
│   └── utils.py                     # Validation helpers
├── main.py                          # Reproducible entry point
├── requirements.txt                 # Dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## How to Run

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline (load → clean → features → export → visualise)
python main.py

# 4. Or open the notebook for the interactive EDA
jupyter notebook notebooks/eda.ipynb
```

## Modular Functions in `src/` (11 functions)

| Function | File | Description |
|---|---|---|
| `load_csv()` | `src/io.py` | Load CSV with encoding support |
| `clean()` | `src/cleaning.py` | 10-step cleaning pipeline |
| `build_features()` | `src/features.py` | Create 3 engineered features |
| `plot_age_distribution()` | `src/viz.py` | Age histogram with KDE |
| `plot_top_companies()` | `src/viz.py` | Top N companies bar chart |
| `plot_gender_by_age_group()` | `src/viz.py` | Gender split stacked bar |
| `plot_company_size_distribution()` | `src/viz.py` | Company size pie chart |
| `plot_tenure_by_age_group()` | `src/viz.py` | Tenure boxplot by age group |
| `assert_columns()` | `src/utils.py` | Validate required columns exist |
| `null_summary()` | `src/utils.py` | Summarise null values |
| `assert_no_full_null_columns()` | `src/utils.py` | Check no column is 100% null |

## Key Findings

1. **Mid-career dominated:** 65% of profiles are aged 31–50 (mean age ~38). LinkedIn adoption is highest among established professionals.
2. **Gender imbalance worsens with seniority:** Male-to-female ratio is ~2:1 overall, but the gap widens significantly in the 41–50 and 51+ age brackets.
3. **Older professionals stay longer:** Median tenure roughly doubles from ~12 months (age 20–30) to ~30 months (age 51+). Younger professionals change jobs more frequently.

## Cleaning Highlights

- Dropped **25 junk/irrelevant columns** (unnamed, URLs, URNs, image data)
- Fixed **corrupted categorical values** in `country`, `genderEstimate`, and `isPremium` caused by row shifts in the original scraping
- Converted `connectionsCount` and `companyStaffCount` from text to numeric
- Parsed `startDate` and `endDate` from strings to datetime
- Removed **48 duplicate rows**

## Remaining Null Values (By Design)

After cleaning, some columns still contain null values — this is **intentional**. The pipeline removes broken data but preserves legitimately absent data:

| Column | Null % | Reason |
|---|---|---|
| `posLocation` | 28.2% | Not recorded in the original LinkedIn scrape |
| `endDate` | 22.5% | NaT means the person is **still in that role** — not missing |
| `genderEstimate` | 10.1% | Algorithm could not classify these profiles; imputing would introduce bias |
| `companyFollowerCount` | 3.7% | Not available for all companies |
| `companyStaffCount` | 2.9% | Not available for all companies |
| Others | <2.3% | Small counts of genuinely absent scraped data |

Dropping all rows with any null would discard a large portion of the dataset for no benefit. Instead, downstream functions apply `dropna` only on the columns they need (e.g., `plot_tenure_by_age_group` drops rows missing `tenure_months` before plotting).
