-- ============================================================
-- Financial Reporting Analysis Queries
-- Database table: financial_reporting_cleaned
-- ============================================================


-- ============================================================
-- 1. Data quality audit queries
-- ============================================================

-- Check remaining duplicate records
SELECT
    Date,
    Agence,
    Activité,
    CA_Réalisé,
    Budget_CA,
    Charges_Réelles,
    Budget_Charges,
    Nombre_Clients,
    Nombre_Missions,
    Heures_Facturées,
    COUNT(*) AS duplicate_count
FROM financial_reporting_cleaned
GROUP BY
    Date,
    Agence,
    Activité,
    CA_Réalisé,
    Budget_CA,
    Charges_Réelles,
    Budget_Charges,
    Nombre_Clients,
    Nombre_Missions,
    Heures_Facturées
HAVING COUNT(*) > 1;


-- Check missing values in critical fields
SELECT *
FROM financial_reporting_cleaned
WHERE Activité IS NULL
   OR CA_Réalisé IS NULL;


-- Check invalid agency names
SELECT DISTINCT Agence
FROM financial_reporting_cleaned
WHERE Agence NOT IN (
    'Paris',
    'Nanterre',
    'Boulogne',
    'Saint-Denis',
    'Créteil'
);


-- Check negative actual expenses
SELECT *
FROM financial_reporting_cleaned
WHERE Charges_Réelles < 0;


-- Check abnormal client counts
SELECT *
FROM financial_reporting_cleaned
WHERE Nombre_Clients > 200;


-- ============================================================
-- 2. Financial analysis queries
-- ============================================================

-- Revenue by agency
SELECT
    Agence,
    ROUND(SUM(CA_Réalisé), 2) AS total_revenue
FROM financial_reporting_cleaned
GROUP BY Agence
ORDER BY total_revenue DESC;


-- Actual margin by agency
SELECT
    Agence,
    ROUND(SUM(Marge_Réelle), 2) AS total_actual_margin
FROM financial_reporting_cleaned
GROUP BY Agence
ORDER BY total_actual_margin DESC;


-- Revenue and margin by activity
SELECT
    Activité,
    ROUND(SUM(CA_Réalisé), 2) AS total_revenue,
    ROUND(SUM(Marge_Réelle), 2) AS total_actual_margin,
    ROUND(AVG(Taux_Marge), 4) AS average_margin_rate
FROM financial_reporting_cleaned
GROUP BY Activité
ORDER BY total_actual_margin DESC;


-- Budget variance by agency
SELECT
    Agence,
    ROUND(SUM(CA_Réalisé), 2) AS total_actual_revenue,
    ROUND(SUM(Budget_CA), 2) AS total_budget_revenue,
    ROUND(SUM(Écart_CA), 2) AS revenue_variance
FROM financial_reporting_cleaned
GROUP BY Agence
ORDER BY revenue_variance DESC;


-- Monthly revenue trend
SELECT
    strftime('%Y-%m', Date) AS month,
    ROUND(SUM(CA_Réalisé), 2) AS total_revenue,
    ROUND(SUM(Marge_Réelle), 2) AS total_actual_margin
FROM financial_reporting_cleaned
GROUP BY month
ORDER BY month;


-- Top 10 records by margin rate
SELECT
    Date,
    Agence,
    Activité,
    ROUND(CA_Réalisé, 2) AS actual_revenue,
    ROUND(Marge_Réelle, 2) AS actual_margin,
    ROUND(Taux_Marge, 4) AS margin_rate
FROM financial_reporting_cleaned
ORDER BY Taux_Marge DESC
LIMIT 10;