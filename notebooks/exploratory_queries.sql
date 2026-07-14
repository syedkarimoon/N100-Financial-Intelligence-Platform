-- ======================================
-- Exploratory Queries - Sprint 1
-- ======================================

-- 1. Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. List Companies
SELECT id,
       company_name
FROM companies
ORDER BY company_name;

-- 3. Total Profit & Loss Records
SELECT COUNT(*) AS total_profit_records
FROM profit_and_loss;

-- 4. Total Balance Sheet Records
SELECT COUNT(*) AS total_balance_records
FROM balance_sheet;

-- 5. Total Cash Flow Records
SELECT COUNT(*) AS total_cashflow_records
FROM cash_flow;

-- 6. Top 10 Companies by Sales
SELECT company_id,
       year,
       sales
FROM profit_and_loss
ORDER BY sales DESC
LIMIT 10;

-- 7. Top 10 Companies by Net Profit
SELECT company_id,
       year,
       net_profit
FROM profit_and_loss
ORDER BY net_profit DESC
LIMIT 10;

-- 8. Companies with Highest ROE
SELECT company_name,
       roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- 9. Companies with Highest ROCE
SELECT company_name,
       roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- 10. Highest Total Assets
SELECT company_id,
       year,
       total_assets
FROM balance_sheet
ORDER BY total_assets DESC
LIMIT 10;