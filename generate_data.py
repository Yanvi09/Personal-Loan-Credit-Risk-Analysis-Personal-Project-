"""
Generates a realistic synthetic personal loan / credit risk dataset.
Self-generated with realistic relationships between income, credit score, loan
amount, and default risk (not random noise) so the analysis behaves like a real
credit portfolio would.
"""
import numpy as np
import pandas as pd

np.random.seed(7)

N = 10000

cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Chennai", "Kolkata", "Ahmedabad"]
employment_types = ["Salaried", "Self-Employed", "Business Owner", "Freelancer"]
employment_weights = [0.55, 0.20, 0.15, 0.10]
loan_purposes = ["Personal", "Home Renovation", "Vehicle", "Education", "Medical", "Business Expansion", "Debt Consolidation"]
purpose_weights = [0.28, 0.14, 0.16, 0.10, 0.08, 0.14, 0.10]

rows = []
for i in range(N):
    customer_id = f"CR{200000+i}"
    age = int(np.clip(np.random.normal(35, 9), 21, 65))
    city = np.random.choice(cities)
    employment_type = np.random.choice(employment_types, p=employment_weights)

    # Income correlated with age (rises then plateaus) and employment type
    base_income = np.random.gamma(shape=3.2, scale=15000)
    age_factor = 1 + min((age - 21) / 40, 0.6)
    employment_factor = {"Salaried": 1.0, "Self-Employed": 1.1, "Business Owner": 1.3, "Freelancer": 0.85}[employment_type]
    monthly_income = round(base_income * age_factor * employment_factor, 2)
    monthly_income = max(15000, monthly_income)

    # Credit score: correlated loosely with income and age (proxy for financial stability)
    credit_score_base = 550 + (monthly_income / 3000) + (age - 21) * 1.2
    credit_score = int(np.clip(np.random.normal(credit_score_base, 45), 300, 900))

    tenure_months = int(np.random.choice([12, 24, 36, 48, 60, 84], p=[0.15,0.22,0.25,0.18,0.12,0.08]))
    loan_purpose = np.random.choice(loan_purposes, p=purpose_weights)

    # Loan amount: some multiple of income, capped by a rough affordability logic
    loan_amount = round(monthly_income * np.random.uniform(3, 14), 2)

    existing_loans = np.random.poisson(0.8)
    dti_ratio = round(min(0.85, (loan_amount / tenure_months) / monthly_income + existing_loans * 0.05 + np.random.uniform(-0.05, 0.05)), 3)
    dti_ratio = max(0.02, dti_ratio)

    # Default probability driven by credit score, DTI ratio, and existing loans (realistic risk model)
    risk_score = (
        (750 - credit_score) / 450 * 0.32
        + dti_ratio * 0.22
        + existing_loans * 0.03
        + (0.04 if employment_type == "Freelancer" else 0)
        - 0.08
    )
    default_prob = np.clip(risk_score, 0.01, 0.9)
    is_default = np.random.random() < default_prob

    rows.append([
        customer_id, age, city, employment_type, monthly_income, credit_score,
        tenure_months, loan_purpose, loan_amount, existing_loans, dti_ratio, int(is_default)
    ])

df = pd.DataFrame(rows, columns=[
    "customer_id", "age", "city", "employment_type", "monthly_income_inr", "credit_score",
    "tenure_months", "loan_purpose", "loan_amount_inr", "existing_loans", "dti_ratio", "is_default"
])

df.to_csv("/home/claude/credit-risk-analytics/data/loan_applications.csv", index=False)
print(f"Generated {len(df)} rows")
print(df.head())
print("\nDefault rate:", round(df["is_default"].mean()*100, 2), "%")
