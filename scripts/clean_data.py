import pandas as pd
import numpy as np
import os

print("Starting data cleaning...")

# ---- Load the raw data ----
# We are reading the CSV file we just created
df = pd.read_csv('../data/crm_raw_data.csv')

print(f"Raw data loaded! Total rows: {len(df)}")

# ---- Step 1: Remove Duplicates ----
# Why? Duplicate rows give wrong counts in reports
# Example: same lead counted twice = wrong conversion rate!
df = df.drop_duplicates()
print(f"After removing duplicates: {len(df)} rows")

# ---- Step 2: Handle Missing Values ----
# Why? Empty cells break calculations and charts
# We fill missing numbers with 0
# We fill missing text with 'Unknown'
df['Number_of_Calls'] = df['Number_of_Calls'].fillna(0)
df['Number_of_Emails'] = df['Number_of_Emails'].fillna(0)
df['Response'] = df['Response'].fillna('No Response')

print("Missing values handled!")

# ---- Step 3: Fix Data Types ----
# Why? Python reads dates as text by default
# We need to tell it "this is a DATE column"
df['Date_Created'] = pd.to_datetime(df['Date_Created'])

print("Date column fixed!")

# ---- Step 4: Create New Features ----
# Why? These new columns help our ML model
# and make our dashboard more powerful!

# Engagement Score = how active is this lead?
# More calls + more emails = higher engagement
df['Engagement_Score'] = (
    df['Number_of_Calls'] * 2 +
    df['Number_of_Emails'] * 1.5
).round(2)

# Recency = how recent was last interaction?
# Lower days = more recent = better lead!
df['Recency'] = df['Last_Interaction_Days'].apply(
    lambda x: 'Hot' if x <= 30
    else 'Warm' if x <= 90
    else 'Cold'
)

# Lead Age = how many days since lead was created?
df['Lead_Age_Days'] = (
    pd.Timestamp.today() - df['Date_Created']
).dt.days

print("New features created!")

# ---- Step 5: Save Clean Data ----
save_path = os.path.join('..', 'data', 'crm_clean_data.csv')
df.to_csv(save_path, index=False)

print("Clean data saved!")
print(f"Final rows: {len(df)}")
print(f"Columns now: {list(df.columns)}")