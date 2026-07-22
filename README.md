# Personal Loan Credit Risk Analysis

A personal data analytics project that explores credit default risk using SQL, Python, Pandas, and Matplotlib.

The project analyzes **10,000 simulated personal loan applications** to identify which borrower characteristics are most strongly associated with loan defaults and demonstrates a complete analytics workflow—from dataset generation to SQL analysis, visualization, and business insights.

> **Note:** The dataset is synthetically generated for learning purposes. Relationships between borrower attributes and default probability were intentionally modeled to resemble realistic lending behavior since real banking datasets are not publicly available.

---

## Objectives

- Analyze a portfolio of personal loan applications
- Identify the strongest predictors of loan default
- Practice SQL aggregation and analytical queries
- Build visualizations to communicate portfolio risk
- Generate business-oriented insights from data

---

## Dataset

The project uses a self-generated dataset containing **10,000 loan applications** with borrower demographics, financial information, loan details, and repayment outcomes.

### Features

- Age
- City
- Employment Type
- Monthly Income
- Credit Score
- Existing Loan Count
- Debt-to-Income Ratio (DTI)
- Loan Purpose
- Loan Amount
- Interest Rate
- Loan Term
- Default Status

---

## Tools & Technologies

- Python
- Pandas
- SQLite
- SQL
- NumPy
- Matplotlib

---

## Analysis Performed

The project uses SQL and Pandas to analyze portfolio risk across multiple borrower segments.

### Credit Score Analysis

- Compared default rates across credit score bands
- Measured average loan amounts by credit segment

### Debt-to-Income (DTI) Analysis

- Grouped borrowers into DTI ranges
- Evaluated how default rates change with increasing debt burden

### Employment Analysis

- Compared default rates across employment types
- Calculated average monthly income by employment category

### Loan Purpose Analysis

- Measured portfolio distribution by loan purpose
- Compared disbursed amounts and default rates

### Existing Loan Analysis

- Evaluated how additional outstanding loans affect default probability

### Geographic Analysis

- Compared portfolio risk across major Indian cities

### Age Analysis

- Compared default rates across borrower age groups

---

# Key Findings

## Portfolio Summary

- **Applications analyzed:** 10,000
- **Total loan portfolio:** ₹566.16 crore
- **Overall default rate:** 14.04%
- **Estimated default exposure:** ₹81.97 crore

---

## Credit Score

| Credit Band | Default Rate |
|-------------|-------------:|
| Poor (<580) | 17.21% |
| Fair (580–669) | 12.10% |
| Good (670–739) | 7.29% |
| Very Good (740–799) | 0.00%* |

\*Very Good contains very few observations in the simulated dataset.

---

## Debt-to-Income Ratio

| DTI Band | Default Rate |
|----------|-------------:|
| 0–20% | 8.81% |
| 20–40% | 12.96% |
| 40–60% | 18.92% |
| 60%+ | 25.20% |

Borrowers in the highest DTI band are approximately **2.9× more likely** to default than borrowers in the lowest DTI band.

---

## Existing Loans

Default rates increase consistently as the number of existing loans increases, indicating existing debt burden is an important secondary risk indicator.

---

## Employment Type

Freelancers exhibit the highest default rate in the dataset, while salaried and business-owner borrowers show comparatively lower risk.

---

## City-Level Analysis

Default rates vary only slightly across cities, suggesting geography is a weaker predictor of default than financial variables such as credit score and DTI.

---

# Business Insights

Based on this simulated portfolio:

- Credit Score and Debt-to-Income Ratio are the strongest predictors of default.
- Existing loan count provides additional risk information.
- Employment type has moderate predictive value.
- City and loan purpose contribute relatively little to risk segmentation.

These findings illustrate how borrower segmentation can support data-driven lending decisions and credit risk assessment.

---

# Project Structure

```
credit-risk-analytics/
│
├── data/
│   └── loan_applications.csv
│
├── sql/
│   └── analysis_queries.sql
│
├── charts/
│
├── generate_data.py
├── run_analysis.py
├── README.md
```

---

# Output

Running

```bash
python run_analysis.py
```

produces:

- SQL analysis summaries
- Portfolio statistics
- Risk segmentation tables
- PNG charts saved to the `charts/` directory

---

# Charts Generated

- Default Rate by Credit Score
- Default Rate by DTI Band
- Default Rate by Employment Type
- Portfolio Risk by City
- Loan Disbursement by Purpose

---

# Skills Demonstrated

- SQL Aggregation
- CASE Statements
- GROUP BY
- Data Cleaning with Pandas
- Portfolio Risk Analysis
- Exploratory Data Analysis (EDA)
- Data Visualization
- Business Insight Generation
