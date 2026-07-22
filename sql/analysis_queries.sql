-- Credit Risk Portfolio Analysis — Core Risk Queries
-- Run against the `loans` table loaded from loan_applications.csv

-- 1. Overall portfolio default rate
SELECT COUNT(*) AS total_loans,
       SUM(is_default) AS total_defaults,
       ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct
FROM loans;

-- 2. Default rate by credit score band
SELECT
  CASE
    WHEN credit_score < 580 THEN 'Poor (<580)'
    WHEN credit_score < 670 THEN 'Fair (580-669)'
    WHEN credit_score < 740 THEN 'Good (670-739)'
    WHEN credit_score < 800 THEN 'Very Good (740-799)'
    ELSE 'Excellent (800+)'
  END AS credit_band,
  COUNT(*) AS loan_count,
  ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct,
  ROUND(AVG(loan_amount_inr), 2) AS avg_loan_amount
FROM loans
GROUP BY credit_band
ORDER BY default_rate_pct DESC;

-- 3. Default rate by DTI (debt-to-income) ratio band
SELECT
  CASE
    WHEN dti_ratio < 0.2 THEN '0-20%'
    WHEN dti_ratio < 0.4 THEN '20-40%'
    WHEN dti_ratio < 0.6 THEN '40-60%'
    ELSE '60%+'
  END AS dti_band,
  COUNT(*) AS loan_count,
  ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY dti_band
ORDER BY dti_band;

-- 4. Default rate by employment type
SELECT employment_type,
       COUNT(*) AS loan_count,
       ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct,
       ROUND(AVG(monthly_income_inr), 2) AS avg_monthly_income
FROM loans
GROUP BY employment_type
ORDER BY default_rate_pct DESC;

-- 5. Default rate and portfolio size by loan purpose
SELECT loan_purpose,
       COUNT(*) AS loan_count,
       ROUND(SUM(loan_amount_inr), 2) AS total_disbursed,
       ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY loan_purpose
ORDER BY total_disbursed DESC;

-- 6. High-risk segment: number of existing loans vs default rate
SELECT existing_loans,
       COUNT(*) AS loan_count,
       ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY existing_loans
ORDER BY existing_loans;

-- 7. City-level portfolio risk
SELECT city,
       COUNT(*) AS loan_count,
       ROUND(SUM(loan_amount_inr), 2) AS total_disbursed,
       ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY city
ORDER BY default_rate_pct DESC;

-- 8. Age band vs default rate
SELECT
  CASE
    WHEN age < 25 THEN '21-24'
    WHEN age < 35 THEN '25-34'
    WHEN age < 45 THEN '35-44'
    WHEN age < 55 THEN '45-54'
    ELSE '55-65'
  END AS age_band,
  COUNT(*) AS loan_count,
  ROUND(100.0 * SUM(is_default) / COUNT(*), 2) AS default_rate_pct
FROM loans
GROUP BY age_band
ORDER BY age_band;
