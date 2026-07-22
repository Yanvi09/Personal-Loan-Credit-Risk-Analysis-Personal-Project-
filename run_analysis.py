"""
Runs SQL risk analysis queries against the loan applications dataset using sqlite3,
and generates supporting charts with matplotlib.
"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "loan_applications.csv")
CHART_DIR = os.path.join(BASE_DIR, "charts")
df = pd.read_csv(DATA_PATH)

conn = sqlite3.connect(":memory:")
df.to_sql("loans", conn, index=False, if_exists="replace")

def run(label, query):
    print(f"\n===== {label} =====")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result

overall = run("Overall Portfolio Default Rate", """
    SELECT COUNT(*) AS total_loans, SUM(is_default) AS total_defaults,
           ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct
    FROM loans
""")

credit_band = run("Default Rate by Credit Score Band", """
    SELECT CASE WHEN credit_score<580 THEN 'Poor (<580)'
                WHEN credit_score<670 THEN 'Fair (580-669)'
                WHEN credit_score<740 THEN 'Good (670-739)'
                WHEN credit_score<800 THEN 'Very Good (740-799)'
                ELSE 'Excellent (800+)' END AS credit_band,
           COUNT(*) AS loan_count, ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct,
           ROUND(AVG(loan_amount_inr),2) AS avg_loan_amount
    FROM loans GROUP BY credit_band ORDER BY default_rate_pct DESC
""")

dti_band = run("Default Rate by DTI Band", """
    SELECT CASE WHEN dti_ratio<0.2 THEN '0-20%'
                WHEN dti_ratio<0.4 THEN '20-40%'
                WHEN dti_ratio<0.6 THEN '40-60%'
                ELSE '60%+' END AS dti_band,
           COUNT(*) AS loan_count, ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct
    FROM loans GROUP BY dti_band ORDER BY dti_band
""")

employment = run("Default Rate by Employment Type", """
    SELECT employment_type, COUNT(*) AS loan_count,
           ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct,
           ROUND(AVG(monthly_income_inr),2) AS avg_monthly_income
    FROM loans GROUP BY employment_type ORDER BY default_rate_pct DESC
""")

purpose = run("Default Rate & Disbursement by Loan Purpose", """
    SELECT loan_purpose, COUNT(*) AS loan_count, ROUND(SUM(loan_amount_inr),2) AS total_disbursed,
           ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct
    FROM loans GROUP BY loan_purpose ORDER BY total_disbursed DESC
""")

existing_loans = run("Default Rate by Existing Loans", """
    SELECT existing_loans, COUNT(*) AS loan_count,
           ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct
    FROM loans GROUP BY existing_loans ORDER BY existing_loans
""")

city_risk = run("City-Level Portfolio Risk", """
    SELECT city, COUNT(*) AS loan_count, ROUND(SUM(loan_amount_inr),2) AS total_disbursed,
           ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct
    FROM loans GROUP BY city ORDER BY default_rate_pct DESC
""")

age_band = run("Default Rate by Age Band", """
    SELECT CASE WHEN age<25 THEN '21-24' WHEN age<35 THEN '25-34'
                WHEN age<45 THEN '35-44' WHEN age<55 THEN '45-54'
                ELSE '55-65' END AS age_band,
           COUNT(*) AS loan_count, ROUND(100.0*SUM(is_default)/COUNT(*),2) AS default_rate_pct
    FROM loans GROUP BY age_band ORDER BY age_band
""")

total_disbursed = round(df["loan_amount_inr"].sum(), 2)
default_loss_estimate = round(df.loc[df.is_default==1, "loan_amount_inr"].sum(), 2)
print(f"\nTotal portfolio disbursed: INR {total_disbursed:,.2f}")
print(f"Estimated exposure in defaulted loans: INR {default_loss_estimate:,.2f}")
print(f"Total applications analyzed: {len(df):,}")

# ---------- Charts ----------
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

# Chart 1: Default rate by credit score band
order = ["Poor (<580)", "Fair (580-669)", "Good (670-739)", "Very Good (740-799)", "Excellent (800+)"]
credit_band_sorted = credit_band.set_index("credit_band").reindex(order).reset_index()
plt.figure(figsize=(8,5))
plt.bar(credit_band_sorted["credit_band"], credit_band_sorted["default_rate_pct"], color="#C53030")
plt.title("Default Rate by Credit Score Band")
plt.ylabel("Default Rate (%)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/default_rate_by_credit_band.png", dpi=150)
plt.close()

# Chart 2: Default rate by DTI band
plt.figure(figsize=(7,5))
plt.bar(dti_band["dti_band"], dti_band["default_rate_pct"], color="#DD6B20")
plt.title("Default Rate by Debt-to-Income (DTI) Ratio")
plt.ylabel("Default Rate (%)")
plt.xlabel("DTI Ratio Band")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/default_rate_by_dti.png", dpi=150)
plt.close()

# Chart 3: Portfolio disbursement by loan purpose
plt.figure(figsize=(8,6))
plt.barh(purpose["loan_purpose"], purpose["total_disbursed"], color="#2C7A7B")
plt.title("Total Disbursed Amount by Loan Purpose")
plt.xlabel("Total Disbursed (INR)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/disbursement_by_purpose.png", dpi=150)
plt.close()

# Chart 4: Default rate by employment type
plt.figure(figsize=(7,5))
plt.bar(employment["employment_type"], employment["default_rate_pct"], color="#805AD5")
plt.title("Default Rate by Employment Type")
plt.ylabel("Default Rate (%)")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/default_rate_by_employment.png", dpi=150)
plt.close()

# Chart 5: City-level risk
plt.figure(figsize=(8,5))
plt.bar(city_risk["city"], city_risk["default_rate_pct"], color="#3182CE")
plt.title("Default Rate by City")
plt.ylabel("Default Rate (%)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/default_rate_by_city.png", dpi=150)
plt.close()

print("\nCharts saved to:", CHART_DIR)
