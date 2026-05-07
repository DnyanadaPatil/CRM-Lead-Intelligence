import pandas as pd
import numpy as np
from faker import Faker
import random
import os

print("Starting...")

fake = Faker()
np.random.seed(42)
random.seed(42)

lead_sources = ['LinkedIn', 'Cold Call', 'Website', 'Referral', 'Email Campaign']
regions = ['North', 'South', 'East', 'West', 'Central']
industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Education']
company_sizes = ['Small', 'Medium', 'Large', 'Enterprise']
sales_agents = ['Amit', 'Priya', 'Rahul', 'Sneha', 'Vikram', 'Neha']

print("Options defined!")

records = []
for i in range(1, 1001):
    converted = random.choices([0, 1], weights=[65, 35])[0]
    deal_value = round(random.uniform(5000, 150000), 2) if converted else 0
    record = {
        'Lead_ID': f'LEAD_{i:04d}',
        'Lead_Source': random.choice(lead_sources),
        'Region': random.choice(regions),
        'Industry': random.choice(industries),
        'Company_Size': random.choice(company_sizes),
        'Sales_Agent': random.choice(sales_agents),
        'Number_of_Calls': random.randint(0, 20),
        'Number_of_Emails': random.randint(0, 30),
        'Last_Interaction_Days': random.randint(1, 180),
        'Contacted': random.choice(['Yes', 'No']),
        'Response': random.choice(['Positive', 'Negative', 'No Response']),
        'Converted': converted,
        'Deal_Value': deal_value,
        'Date_Created': fake.date_between(start_date='-2y', end_date='today')
    }
    records.append(record)

print("1000 records created!")

df = pd.DataFrame(records)

for col in ['Number_of_Calls', 'Number_of_Emails', 'Response']:
    null_indices = random.sample(range(1000), 30)
    df.loc[null_indices, col] = np.nan

duplicates = df.sample(20)
df = pd.concat([df, duplicates], ignore_index=True)

print("Messy data added!")

save_path = os.path.join('..', 'data', 'crm_raw_data.csv')
df.to_csv(save_path, index=False)

print("Dataset saved successfully!")
print(f"Total records: {len(df)}")
print(f"Columns: {list(df.columns)}")