import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import os

print("Starting ML model...")

# ---- Load Clean Data ----
df = pd.read_csv('../data/crm_clean_data.csv')
print(f"Data loaded! Rows: {len(df)}")

# ---- Save original text columns for later ----
# Why? We need numbers for ML but readable text for reports
df_original = df.copy()

# ---- Prepare Features ----
# ML models only understand NUMBERS
# So we convert text columns to numbers
le = LabelEncoder()
text_columns = ['Lead_Source', 'Region', 'Industry',
                'Company_Size', 'Contacted', 'Response', 'Recency']

for col in text_columns:
    df[col] = le.fit_transform(df[col])

print("Text columns converted to numbers!")

# ---- Select Features for Model ----
features = [
    'Lead_Source', 'Region', 'Industry', 'Company_Size',
    'Number_of_Calls', 'Number_of_Emails',
    'Last_Interaction_Days', 'Contacted', 'Response',
    'Engagement_Score', 'Lead_Age_Days'
]

target = 'Converted'

X = df[features]
y = df[target]

print(f"Features selected: {len(features)} columns")

# ---- Split Data ----
# 80% training, 20% testing
# Like studying from textbook and giving exam!
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")

# ---- Train the Model ----
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("Model trained!")

# ---- Check Accuracy ----
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {round(accuracy * 100, 2)}%")

# ---- Generate Lead Scores ----
df_original['Conversion_Probability'] = model.predict_proba(X[features])[:, 1]
df_original['Lead_Score'] = (df_original['Conversion_Probability'] * 100).round(2)

# ---- Decision Engine ----
# Based on score we suggest what action to take
# Thresholds based on actual score distribution
# Max score = 48.96, Mean = 36.37
def get_recommendation(score, last_interaction):
    if score >= 42 and last_interaction <= 45:
        return 'Call Immediately'
    elif score >= 42 and last_interaction > 45:
        return 'Re-engage Urgently'
    elif score >= 33:
        return 'Send Follow-up Email'
    else:
        return 'Low Priority - Nurture'

df_original['Recommendation'] = df_original.apply(
    lambda row: get_recommendation(
        row['Lead_Score'],
        row['Last_Interaction_Days']
    ), axis=1
)

print("Lead scores and recommendations generated!")
print(df_original['Recommendation'].value_counts())

# ---- Save Final Output ----
save_path = os.path.join('..', 'data', 'crm_scored_data.csv')
df_original.to_csv(save_path, index=False)

print("Final scored data saved!")
print(f"Columns: {list(df_original.columns)}")