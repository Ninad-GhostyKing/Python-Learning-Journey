import pandas as pd

df = pd.read_csv("Day72-81/Day72/Learning_Pandas/data/salaries_by_college_major.csv")

df.head()

df.shape

df.columns

df.isna()

df.tail()

clean_df = df.dropna()

clean_df.tail()

clean_df["Starting Median Salary"].max()

clean_df["Starting Median Salary"].idxmax()

clean_df["Undergraduate Major"].loc[43]
clean_df["Undergraduate Major"][43]

clean_df.loc[43]

# CHALLENGE
# 1. What college major has the highest mid-career salary? How much do graduates with this major earn?
clean_df.loc[clean_df["Mid-Career Median Salary"].idxmax()]

# 2. Which college major has the lowest starting salary and how much do graduates earn after university?
clean_df.loc[clean_df["Starting Median Salary"].idxmin()]

# 3. Which college major has the lowest mid-career salary and how much can people expect to earn with this degree?
clean_df.loc[clean_df["Mid-Career Median Salary"].idxmin()]

# ----- xxxxx -----


spread_col = (
    clean_df["Mid-Career 90th Percentile Salary"]
    - clean_df["Mid-Career 10th Percentile Salary"]
)

clean_df["Mid-Career 90th Percentile Salary"].subtract(
    clean_df["Mid-Career 10th Percentile Salary"]
)

clean_df.insert(1, "Spread", spread_col)
clean_df.head()

clean_df.drop(columns="Spread", axis=1, inplace=True)

low_risk = clean_df.sort_values("Spread")
low_risk[["Undergraduate Major", "Spread"]].head()

# CHALLENGE

highest_potential = clean_df.sort_values(
    "Mid-Career 90th Percentile Salary", ascending=False
)
highest_potential[["Undergraduate Major", "Mid-Career 90th Percentile Salary"]].head()

greatest_spread = clean_df.sort_values("Spread", ascending=False)
greatest_spread[["Undergraduate Major", "Spread"]].head()

# ----- xxxxx ------

clean_df.groupby("Group").count()

# clean_df.groupby("Group").mean() # doesnt seem to work for me.

pd.options.display.float_format = "{:,.2f}".format
