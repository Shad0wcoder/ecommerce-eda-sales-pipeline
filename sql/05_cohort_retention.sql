-- Customer Monthly Purchases
WITH customer_months AS (

    SELECT DISTINCT
        customer_id,
        DATE_TRUNC(
            'month',
            order_date
        ) AS purchase_month

    FROM orders

    WHERE order_status = 'Completed'
),


-- First Purchase Month

first_purchase AS (

    SELECT
        customer_id,
        MIN(purchase_month) AS cohort_month

    FROM customer_months

    GROUP BY customer_id
),


-- Cohort Activity

cohort_activity AS (

    SELECT
        cm.customer_id,
        fp.cohort_month,
        cm.purchase_month,

        (
            EXTRACT(
                YEAR FROM cm.purchase_month
            )
            - EXTRACT(
                YEAR FROM fp.cohort_month
            )
        ) * 12
        +
        (
            EXTRACT(
                MONTH FROM cm.purchase_month
            )
            - EXTRACT(
                MONTH FROM fp.cohort_month
            )
        ) AS month_number

    FROM customer_months cm

    JOIN first_purchase fp
        ON cm.customer_id = fp.customer_id
),


-- Active Customers Per Cohort

cohort_counts AS (

    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT customer_id)
            AS active_customers

    FROM cohort_activity

    GROUP BY
        cohort_month,
        month_number
),


-- Cohort Size

cohort_sizes AS (

    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id)
            AS cohort_size

    FROM first_purchase

    GROUP BY cohort_month
)

SELECT
    cc.cohort_month,
    cc.month_number,
    cc.active_customers,
    cs.cohort_size,

    ROUND(
        cc.active_customers * 100.0
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS retention_rate

FROM cohort_counts cc

JOIN cohort_sizes cs
    ON cc.cohort_month = cs.cohort_month

ORDER BY
    cc.cohort_month,
    cc.month_number;