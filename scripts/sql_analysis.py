import pandas as pd
import sqlite3
import os

print("Starting SQL analysis...")

# ---- What is sqlite3? ----
# It's a library that lets us create a database
# and run SQL queries directly in Python!
# No need to install MySQL or PostgreSQL separately

# ---- Load our scored data ----
df = pd.read_csv('../data/crm_scored_data.csv')
print(f"Data loaded! Rows: {len(df)}")

# ---- Create a Database ----
# This creates a .db file (our database)
conn = sqlite3.connect('../data/crm_database.db')
print("Database created!")

# ---- Load our data INTO the database ----
# We are putting our CSV data into a proper SQL table
df.to_sql('leads', conn, if_exists='replace', index=False)
print("Data loaded into database table 'leads'!")

# ---- Helper function to run queries ----
def run_query(title, query):
    print(f"\n{'='*50}")
    print(f"Query: {title}")
    print('='*50)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result

# ---- Query 1: Overall Conversion Rate ----
# Business Question: How many leads are we converting?
q1 = run_query(
    "Overall Conversion Rate",
    """
    SELECT 
        COUNT(*) as Total_Leads,
        SUM(Converted) as Total_Converted,
        ROUND(AVG(Converted) * 100, 2) as Conversion_Rate_Percent
    FROM leads
    """
)

# ---- Query 2: Lead Source Performance ----
# Business Question: Where are our best leads coming from?
q2 = run_query(
    "Lead Source Performance",
    """
    SELECT 
        Lead_Source,
        COUNT(*) as Total_Leads,
        SUM(Converted) as Converted,
        ROUND(AVG(Converted) * 100, 2) as Conversion_Rate,
        ROUND(SUM(Deal_Value), 2) as Total_Revenue
    FROM leads
    GROUP BY Lead_Source
    ORDER BY Conversion_Rate DESC
    """
)

# ---- Query 3: Sales Agent Performance ----
# Business Question: Who is our best sales agent?
q3 = run_query(
    "Sales Agent Performance",
    """
    SELECT 
        Sales_Agent,
        COUNT(*) as Total_Leads,
        SUM(Converted) as Converted,
        ROUND(AVG(Converted) * 100, 2) as Conversion_Rate,
        ROUND(SUM(Deal_Value), 2) as Total_Revenue,
        ROUND(AVG(Lead_Score), 2) as Avg_Lead_Score
    FROM leads
    GROUP BY Sales_Agent
    ORDER BY Total_Revenue DESC
    """
)

# ---- Query 4: Industry Revenue ----
# Business Question: Which industry makes us most money?
q4 = run_query(
    "Industry Revenue Analysis",
    """
    SELECT 
        Industry,
        COUNT(*) as Total_Leads,
        SUM(Converted) as Converted,
        ROUND(SUM(Deal_Value), 2) as Total_Revenue,
        ROUND(AVG(Deal_Value), 2) as Avg_Deal_Value
    FROM leads
    GROUP BY Industry
    ORDER BY Total_Revenue DESC
    """
)

# ---- Query 5: High Priority Leads ----
# Business Question: Which leads should we call RIGHT NOW?
q5 = run_query(
    "Top 10 High Priority Leads",
    """
    SELECT 
        Lead_ID,
        Lead_Source,
        Industry,
        Sales_Agent,
        Lead_Score,
        Recommendation,
        Last_Interaction_Days
    FROM leads
    WHERE Recommendation = 'Call Immediately'
        OR Recommendation = 'Re-engage Urgently'
    ORDER BY Lead_Score DESC
    LIMIT 10
    """
)

# ---- Save results to CSV ----
q2.to_csv('../output/lead_source_performance.csv', index=False)
q3.to_csv('../output/agent_performance.csv', index=False)
q4.to_csv('../output/industry_revenue.csv', index=False)

print("\nAll query results saved to output folder!")

# ---- Close database connection ----
conn.close()
print("Database connection closed!")
print("\nSQL Analysis Complete!")
