from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker



# Configuration


SEED = 500

N_CUSTOMERS = 5000
N_PRODUCTS = 300
N_ORDERS = 20000

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



# Reproducibility


np.random.seed(SEED)

fake = Faker("en_IN")
Faker.seed(SEED)



# Helper functions


def random_date(start_date, end_date, size):
    """
    Generate random timestamps between two dates.
    """
    start = pd.Timestamp(start_date).value // 10**9
    end = pd.Timestamp(end_date).value // 10**9

    timestamps = np.random.randint(start, end, size=size)

    return pd.to_datetime(timestamps, unit="s")



# Customers


def generate_customers():
    customer_ids = [f"CUST{i:05d}" for i in range(1, N_CUSTOMERS + 1)]

    cities = [
        "Delhi",
        "Mumbai",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Kolkata",
        "Ahmedabad",
        "Jaipur",
        "Lucknow",
    ]

    segments = ["Regular", "Premium", "VIP"]

    customers = []

    for customer_id in customer_ids:
        signup_date = fake.date_between(
            start_date="-3y",
            end_date="today",
        )

        customers.append(
            {
                "customer_id": customer_id,
                "customer_name": fake.name(),
                "email": fake.email(),
                "gender": np.random.choice(
                    ["Male", "Female", "Other"],
                    p=[0.48, 0.48, 0.04],
                ),
                "age": int(np.clip(np.random.normal(34, 11), 18, 75)),
                "city": np.random.choice(cities),
                "customer_segment": np.random.choice(
                    segments,
                    p=[0.70, 0.25, 0.05],
                ),
                "signup_date": signup_date,
            }
        )

    df = pd.DataFrame(customers)

    # Introduce a small amount of missing demographic data.
    missing_city = np.random.choice(
        df.index,
        size=int(len(df) * 0.01),
        replace=False,
    )

    df.loc[missing_city, "city"] = np.nan

    return df



# Products


def generate_products():
    categories = {
        "Electronics": 0.20,
        "Fashion": 0.25,
        "Home": 0.20,
        "Beauty": 0.15,
        "Sports": 0.10,
        "Books": 0.10,
    }

    category_names = list(categories.keys())
    category_probabilities = list(categories.values())

    products = []

    for i in range(1, N_PRODUCTS + 1):
        category = np.random.choice(
            category_names,
            p=category_probabilities,
        )

        # Log-normal distribution creates realistic price skew.
        price = np.random.lognormal(
            mean=7.0,
            sigma=0.65,
        )

        price = round(float(np.clip(price, 199, 100000)), 2)

        products.append(
            {
                "product_id": f"PROD{i:04d}",
                "product_name": f"{category} Product {i:04d}",
                "category": category,
                "unit_price": price,
                "cost_price": round(price * np.random.uniform(0.45, 0.75), 2),
                "stock_quantity": int(
                    np.random.lognormal(
                        mean=4,
                        sigma=0.7,
                    )
                ),
            }
        )

    return pd.DataFrame(products)



# Orders


def generate_orders(customers):
    customer_ids = customers["customer_id"].drop_duplicates().tolist()

    # Pareto-like behavior:
    # a smaller percentage of customers generate more orders.
    weights = np.random.pareto(
        a=2.2,
        size=len(customer_ids),
    ) + 1

    weights = weights / weights.sum()

    selected_customers = np.random.choice(
        customer_ids,
        size=N_ORDERS,
        replace=True,
        p=weights,
    )

    order_dates = random_date(
        START_DATE,
        END_DATE,
        N_ORDERS,
    )

    statuses = np.random.choice(
        [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Pending",
            "Cancelled",
            "Returned",
        ],
        size=N_ORDERS,
        p=[
            0.68,
            0.10,
            0.08,
            0.05,
            0.04,
            0.03,
            0.02,
        ],
    )

    payment_methods = np.random.choice(
        [
            "Credit Card",
            "Debit Card",
            "UPI",
            "Net Banking",
            "Cash on Delivery",
        ],
        size=N_ORDERS,
        p=[
            0.20,
            0.15,
            0.40,
            0.10,
            0.15,
        ],
    )

    orders = pd.DataFrame(
        {
            "order_id": [
                f"ORD{i:06d}"
                for i in range(1, N_ORDERS + 1)
            ],
            "customer_id": selected_customers,
            "order_date": order_dates,
            "order_status": statuses,
            "payment_method": payment_methods,
        }
    )

    # Shipping occurs after order date.
    shipping_days = np.random.randint(
        1,
        6,
        size=N_ORDERS,
    )

    orders["shipping_date"] = (
        orders["order_date"]
        + pd.to_timedelta(shipping_days, unit="D")
    )

    # Delivery occurs after shipping.
    delivery_days = np.random.randint(
        1,
        8,
        size=N_ORDERS,
    )

    orders["delivery_date"] = (
        orders["shipping_date"]
        + pd.to_timedelta(delivery_days, unit="D")
    )

    # Cancelled/pending orders often have missing logistics dates.
    mask = orders["order_status"].isin(
        ["Cancelled", "Pending"]
    )

    orders.loc[mask, "shipping_date"] = pd.NaT
    orders.loc[mask, "delivery_date"] = pd.NaT

    # Additional random missing delivery dates.
    missing_delivery = np.random.random(N_ORDERS) < 0.015

    orders.loc[
        missing_delivery,
        "delivery_date",
    ] = pd.NaT

    return orders



# Order Items


def generate_order_items(orders, products):
    rows = []

    product_ids = products["product_id"].tolist()

    product_prices = products.set_index(
        "product_id"
    )["unit_price"].to_dict()

    item_id = 1

    for _, order in orders.iterrows():
        number_of_items = np.random.choice(
            [1, 2, 3, 4, 5],
            p=[0.45, 0.30, 0.15, 0.07, 0.03],
        )

        selected_products = np.random.choice(
            product_ids,
            size=number_of_items,
            replace=False,
        )

        for product_id in selected_products:
            quantity = np.random.choice(
                [1, 2, 3, 4],
                p=[0.65, 0.25, 0.08, 0.02],
            )

            unit_price = product_prices[product_id]

            discount = np.random.choice(
                [0, 5, 10, 15, 20, 25],
                p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
            )

            rows.append(
                {
                    "order_item_id": f"ITEM{item_id:07d}",
                    "order_id": order["order_id"],
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_percent": discount,
                }
            )

            item_id += 1

    return pd.DataFrame(rows)



# Payments


def generate_payments(orders):
    payments = []

    for _, order in orders.iterrows():

        if order["order_status"] == "Cancelled":
            payment_status = "Refunded"

        elif order["order_status"] == "Pending":
            payment_status = np.random.choice(
                ["Pending", "Failed"],
                p=[0.70, 0.30],
            )

        elif order["order_status"] == "Returned":
            payment_status = "Refunded"

        else:
            payment_status = np.random.choice(
                ["Paid", "Failed"],
                p=[0.97, 0.03],
            )

        payments.append(
            {
                "payment_id": f"PAY{len(payments) + 1:07d}",
                "order_id": order["order_id"],
                "payment_date": order["order_date"]
                + pd.Timedelta(
                    days=int(np.random.randint(0, 3))
                ),
                "payment_method": order["payment_method"],
                "payment_status": payment_status,
            }
        )

    return pd.DataFrame(payments)



# Main


def main():
    print("Generating customers...")
    customers = generate_customers()

    print("Generating products...")
    products = generate_products()

    print("Generating orders...")
    orders = generate_orders(customers)

    print("Generating order items...")
    order_items = generate_order_items(
        orders,
        products,
    )

    print("Generating payments...")
    payments = generate_payments(orders)

    # Save CSVs.
    customers.to_csv(
        OUTPUT_DIR / "customers.csv",
        index=False,
    )

    products.to_csv(
        OUTPUT_DIR / "products.csv",
        index=False,
    )

    orders.to_csv(
        OUTPUT_DIR / "orders.csv",
        index=False,
    )

    order_items.to_csv(
        OUTPUT_DIR / "order_items.csv",
        index=False,
    )

    payments.to_csv(
        OUTPUT_DIR / "payments.csv",
        index=False,
    )

    print("\nData generation completed.")
    print(f"Customers:   {len(customers):,}")
    print(f"Products:    {len(products):,}")
    print(f"Orders:      {len(orders):,}")
    print(f"Order items: {len(order_items):,}")
    print(f"Payments:    {len(payments):,}")

    print("\nFiles saved to:")
    print(OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()