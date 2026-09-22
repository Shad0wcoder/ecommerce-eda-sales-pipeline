-- Customer Order Ranking

WITH customer_orders AS (

    SELECT
        o.customer_id,
        o.order_id,
        o.order_date,

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

    GROUP BY
        o.customer_id,
        o.order_id,
        o.order_date
)

SELECT
    customer_id,
    order_id,
    order_date,
    order_value,

    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS order_number,

    RANK() OVER (
        PARTITION BY customer_id
        ORDER BY order_value DESC
    ) AS value_rank

FROM customer_orders

ORDER BY customer_id, order_date;