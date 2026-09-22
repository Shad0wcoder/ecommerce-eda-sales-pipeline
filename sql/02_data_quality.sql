-- Row Counts

SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'products', COUNT(*)
FROM products

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM order_items

UNION ALL

SELECT 'payments', COUNT(*)
FROM payments;


-- Duplicate Customers

SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- Missing Order Dates

SELECT
    COUNT(*) AS total_orders,
    COUNT(*) FILTER (
        WHERE order_date IS NULL
    ) AS missing_order_date,
    COUNT(*) FILTER (
        WHERE shipping_date IS NULL
    ) AS missing_shipping_date,
    COUNT(*) FILTER (
        WHERE delivery_date IS NULL
    ) AS missing_delivery_date
FROM orders;


-- Invalid Quantities

SELECT *
FROM order_items
WHERE quantity <= 0;

-- Invalid Prices


SELECT *
FROM order_items
WHERE unit_price <= 0;


-- Orphan Orders

SELECT o.*
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- Payment Coverage

SELECT
    COUNT(*) AS total_orders,
    COUNT(p.order_id) AS orders_with_payment
FROM orders o
LEFT JOIN payments p
    ON o.order_id = p.order_id;


-- Order Status Distribution

SELECT
    order_status,
    COUNT(*) AS orders,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM orders
GROUP BY order_status
ORDER BY orders DESC;