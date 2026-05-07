# CRM Lead Intelligence & Decision System

Built this to solve a real problem — sales teams waste time chasing the wrong leads. This project scores every lead using machine learning and tells agents exactly what to do next.

## What It Does

Takes 1000 raw CRM records, cleans them, runs a Logistic Regression model to score each lead, and outputs one of four actions — Call Immediately, Re-engage Urgently, Send Follow-up Email, or Low Priority. Everything is visualized in a 4-page interactive Power BI dashboard.

## Tech Stack

Python · Pandas · NumPy · Scikit-learn · SQLite · Power BI

## Key Results

- 1000 leads analyzed with 36.3% overall conversion rate
- Machine learning model achieved 64% accuracy
- 48 leads flagged as Call Immediately by the Decision Engine
- Top agent: Vikram with 40.88% conversion rate and ₹55L revenue
- Best lead source: Website at 40.23% conversion
- Finance industry generated highest revenue at ₹73L

## Dashboard Pages

- Executive Dashboard — KPI cards, monthly trends, region performance
- Lead Funnel Analysis — decision breakdown, recency funnel, lead source chart
- Sales Team Performance — agent revenue and conversion comparison
- Decision Intelligence Panel — lead score vs conversion probability scatter plot

## Project Structure

- scripts/ — data generation, cleaning, ML model, SQL analysis
- data/ — raw, cleaned and scored datasets
- output/ — SQL query results
- CRM_Lead_Intelligence.pbix — Power BI dashboard

B.Tech Artificial Intelligence & Machine Learning · 3rd Year · Dnyanada Patil
