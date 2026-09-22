-- Base Revenue Dataset

WITH order_revenue AS (

    SELECT
        o.order_id,
        o.customer_id,
        DATE(o.order_date) AS order_date,
        o.order_status,

        SUM(
            oi.quantity
            * oi.unit_price
            * (
                1 - oi.discount_percent / 100.0
            )
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'Completed'

    GROUP BY
        o.order_id,
        o.customer_id,
        DATE(o.order_date),
        o.order_status
)

SELECT *
FROM order_revenue
ORDER BY order_date;


-- Monthly Revenue

WITH monthly_sales AS (

    SELECT
        DATE_TRUNC(
            'month',
            o.order_date
        ) AS month,

        SUM(
            oi.quantity
            * oi.unit_price
            * (
                1 - oi.discount_percent / 100.0
            )
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'Completed'

    GROUP BY 1
)

SELECT
    month,
    revenue
FROM monthly_sales
ORDER BY month;


-- MoM Growth

WITH monthly_sales AS (

    SELECT
        DATE_TRUNC(
            'month',
            o.order_date
        ) AS month,

        SUM(
            oi.quantity
            * oi.unit_price
            * (
                1 - oi.discount_percent / 100.0
            )
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'Completed'

    GROUP BY 1
),

with_previous AS (

    SELECT
        month,
        revenue,

        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_revenue

    FROM monthly_sales
)

SELECT
    month,
    revenue,
    previous_revenue,

    ROUND(
        (
            revenue - previous_revenue
        )
        / NULLIF(previous_revenue, 0)
        * 100,
        2
    ) AS mom_growth_percent

FROM with_previous
ORDER BY month;


-- Rolling 30-Day Revenue

WITH daily_sales AS (

    SELECT
        DATE(o.order_date) AS sales_date,

        SUM(
            oi.quantity
            * oi.unit_price
            * (
                1 - oi.discount_percent / 100.0
            )
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'Completed'

    GROUP BY 1
)

SELECT
    sales_date,
    revenue,

    SUM(revenue) OVER (
        ORDER BY sales_date
        ROWS BETWEEN 29 PRECEDING
        AND CURRENT ROW
    ) AS rolling_30_day_revenue

FROM daily_sales

ORDER BY sales_date;


-- Average Order Value

WITH order_values AS (

    SELECT
        o.order_id,

        SUM(
            oi.quantity
            * oi.unit_price
            * (
                1 - oi.discount_percent / 100.0
            )
        ) AS order_value

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'Completed'

    GROUP BY o.order_id
)

SELECT
    COUNT(*) AS completed_orders,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS average_order_value
FROM order_values;