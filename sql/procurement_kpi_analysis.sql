-- Procurement Spend & Supplier Performance Analysis
-- Dialect: PostgreSQL-compatible SQL. Adapt date functions as needed for your DBMS.

-- 1) Executive supplier scorecard
WITH supplier_metrics AS (
    SELECT
        supplier,
        SUM(total_spend) AS total_spend,
        COUNT(*) AS purchase_orders,
        ROUND(100.0 * AVG(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END), 1) AS on_time_delivery_pct,
        ROUND(AVG(days_late), 2) AS avg_days_late,
        ROUND(AVG(quality_score), 1) AS avg_quality_score,
        SUM(CASE WHEN expedite_flag = 'Yes' THEN 1 ELSE 0 END) AS expedited_pos
    FROM procurement_orders
    GROUP BY supplier
)
SELECT
    supplier, total_spend, purchase_orders, on_time_delivery_pct, avg_days_late,
    avg_quality_score, expedited_pos,
    CASE
        WHEN on_time_delivery_pct < 90 OR avg_quality_score < 92 THEN 'Develop / mitigate risk'
        ELSE 'Maintain / grow relationship'
    END AS priority_action
FROM supplier_metrics
ORDER BY total_spend DESC;

-- 2) Category spend, concentration, and service performance
SELECT
    category,
    SUM(total_spend) AS total_spend,
    COUNT(*) AS purchase_orders,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    ROUND(100.0 * AVG(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END), 1) AS on_time_delivery_pct
FROM procurement_orders
GROUP BY category
ORDER BY total_spend DESC;

-- 3) POs requiring buyer intervention
SELECT
    po_number, supplier, category, total_spend, required_delivery_date,
    actual_delivery_date, days_late, expedite_flag, quality_score,
    CASE
        WHEN days_late >= 7 OR expedite_flag = 'Yes' THEN 'High'
        WHEN days_late >= 4 THEN 'Medium'
        ELSE 'Low'
    END AS risk_level
FROM procurement_orders
WHERE days_late >= 4 OR expedite_flag = 'Yes'
ORDER BY
    CASE WHEN days_late >= 7 OR expedite_flag = 'Yes' THEN 1 ELSE 2 END,
    days_late DESC,
    total_spend DESC;

-- 4) Supplier price variance within each category
WITH category_prices AS (
    SELECT category, AVG(unit_price) AS category_avg_price
    FROM procurement_orders
    GROUP BY category
)
SELECT
    p.supplier, p.category,
    ROUND(AVG(p.unit_price), 2) AS supplier_avg_price,
    ROUND(c.category_avg_price, 2) AS category_avg_price,
    ROUND(100.0 * (AVG(p.unit_price) - c.category_avg_price) / c.category_avg_price, 1) AS price_variance_pct,
    SUM(p.total_spend) AS supplier_category_spend
FROM procurement_orders p
JOIN category_prices c ON p.category = c.category
GROUP BY p.supplier, p.category, c.category_avg_price
ORDER BY price_variance_pct DESC, supplier_category_spend DESC;
