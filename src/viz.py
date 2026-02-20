import matplotlib.pyplot as plt
import seaborn as sns


def plot_age_distribution(df):
    """1. Histogram of estimated ages across all LinkedIn profiles."""
    plt.figure(figsize=(10, 5))
    sns.histplot(df["ageEstimate"], bins=30, kde=True, color="steelblue")
    plt.title("Distribution of Estimated Age of LinkedIn Professionals", fontsize=14)
    plt.xlabel("Estimated Age")
    plt.ylabel("Number of Profiles")
    plt.tight_layout()
    plt.show()


def plot_top_companies(df, n=15):
    """2. Horizontal bar chart of the top N companies by number of positions."""
    top = df["companyName"].value_counts().head(n).sort_values()
    plt.figure(figsize=(10, 6))
    top.plot.barh(color="teal")
    plt.title(f"Top {n} Companies by Number of Positions", fontsize=14)
    plt.xlabel("Number of Positions")
    plt.ylabel("Company")
    plt.tight_layout()
    plt.show()


def plot_gender_by_age_group(df):
    """3. Stacked bar chart showing gender split across age groups."""
    ct = df.groupby(["age_group", "genderEstimate"], observed=False).size().unstack(fill_value=0)
    ct.plot.bar(stacked=True, figsize=(9, 5), color=["#4C72B0", "#DD8452"])
    plt.title("Gender Distribution by Age Group", fontsize=14)
    plt.xlabel("Age Group")
    plt.ylabel("Count")
    plt.legend(title="Gender")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_company_size_distribution(df):
    """4. Pie chart of company size categories."""
    counts = df["company_size_category"].value_counts()
    plt.figure(figsize=(7, 7))
    counts.plot.pie(autopct="%1.1f%%", startangle=140,
                    colors=["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3"])
    plt.title("Company Size Distribution", fontsize=14)
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def plot_tenure_by_age_group(df):
    """5. Box plot of position tenure (months) across age groups."""
    subset = df.dropna(subset=["tenure_months", "age_group"])
    subset = subset[subset["tenure_months"].between(0, 200)]
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=subset, x="age_group", y="tenure_months",
                hue="age_group", palette="Set2", legend=False,
                order=["20-30", "31-40", "41-50", "51+"])
    plt.title("Position Tenure (Months) by Age Group", fontsize=14)
    plt.xlabel("Age Group")
    plt.ylabel("Tenure (Months)")
    plt.tight_layout()
    plt.show()
