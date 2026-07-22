# Personal Loan Credit Risk Analysis

Analysis of 10,000 simulated personal loan applications, built to practice
credit risk analytics: identifying which borrower attributes are actually
predictive of default, using SQL and pandas.

> **Note on the data:** This dataset is self-generated with realistic, deliberately
> modeled relationships (default probability driven by credit score, debt-to-income
> ratio, existing loan count, and employment type — not random noise), since real
> loan portfolios aren't publicly available. The queries and analytical approach are
> the same as I'd apply to a real lending dataset.

## What this project covers
- Designing a loan-level schema (12 fields: borrower demographics, financials,
  loan terms, and default outcome)
- Building a risk model with intentional, explainable relationships between
  credit score, DTI ratio, and default probability
- Writing SQL queries (CASE-based risk bucketing, GROUP BY aggregation) to segment
  the portfolio by risk driver
- Quantifying which factors matter most for default prediction

## Key Findings

**Overall Portfolio**
- 10,000 applications, ₹566.2 crore total disbursed, 14.04% overall default rate
- Estimated exposure in defaulted loans: ₹81.97 crore

**Credit Score is the strongest single risk driver**
- Poor credit (<580): 17.21% default rate
- Fair credit (580-669): 12.10% default rate
- Good credit (670-739): 7.29% default rate
- The drop from Poor to Good is a **9.9 percentage point** difference — the clearest
  segmentation variable in the dataset

**DTI ratio shows a clean, monotonic risk gradient**
- 0-20% DTI: 8.81% default rate
- 20-40% DTI: 12.96%
- 40-60% DTI: 18.92%
- 60%+ DTI: 25.20%
- Borrowers in the highest DTI band are **2.9x more likely to default** than
  those in the lowest band — a strong, usable underwriting signal

**Existing loan count compounds risk sharply**
- 0 existing loans: 10.99% default rate
- 3 existing loans: 23.22%
- 4 existing loans: 32.43%
- (Buckets above 4 existing loans have very small sample sizes — under 15 loans each —
  so those specific rates aren't statistically reliable on their own, but the trend
  through 0-4 is consistent and directionally strong)

**Employment type matters, but less than credit score or DTI**
- Freelancers carry the highest default rate (17.76%) despite not having the lowest
  average income — consistent with income *volatility*, not just income level,
  being a risk factor
- Business Owners default least among self-employed categories (13.26%) despite
  having the highest average income, suggesting income stability matters more than
  income size

**City-level risk is relatively flat**
- Default rates range narrowly from 12.98% (Mumbai) to 15.85% (Pune) — geography is
  a weak risk signal compared to credit score or DTI in this portfolio

## Business Recommendation
Credit score and DTI ratio should anchor the underwriting model — both show strong,
monotonic relationships with default risk, unlike city or loan purpose, which are
comparatively flat. Existing loan count is a strong secondary signal, especially for
borrowers with DTI already above 40%, where the two risks likely compound. Freelancer
status is worth a targeted review — not because of income level, but because of income
volatility risk.

## Files
- `generate_data.py` — synthetic dataset generator with documented risk-model logic
- `data/loan_applications.csv` — the dataset (10,000 rows, 12 columns)
- `sql/analysis_queries.sql` — the 8 core SQL risk-segmentation queries
- `run_analysis.py` — runs all SQL queries via sqlite3, prints results, generates charts
- `charts/` — 5 exported PNG charts (default rate by credit band, DTI, employment
  type, city, and disbursement by loan purpose)

## Tech Stack
Python, pandas, SQLite (SQL), matplotlib, NumPy
