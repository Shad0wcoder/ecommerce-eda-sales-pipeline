from pathlib import Path

import numpy as np
import pandas as pd



# Paths


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)



# Load Data


def load_data():
    customers = pd.read_csv(
        RAW_DIR / "customers.csv",
        parse_dates=["signup_date"],
    )

    products = pd.read_csv(
        RAW_DIR / "products.csv",
    )

    orders = pd.read_csv(
        RAW_DIR / "orders.csv",
        parse_dates=[
            "order_date",
            "shipping_date",
            "delivery_date",
        ],
    )

    order_items = pd.read_csv(
        RAW_DIR / "order_items.csv",
    )

    payments = pd.read_csv(
        RAW_DIR / "payments.csv",
        parse_dates=["payment_date"],
    )

    return (
        customers,
        products,
        orders,
        order_items,
        payments,
    )



# Clean Customers


def clean_customers(customers):

    customers = customers.copy()

    customers = customers.drop_duplicates(
        subset=["customer_id"],
        keep="first",
    )

    customers["customer_name"] = (
        customers["customer_name"]
        .fillna("Unknown Customer")
        .astype(str)
        .str.strip()
    )

    customers["email"] = (
        customers["email"]
        .fillna("unknown@example.com")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    customers["city"] = (
        customers["city"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    customers["age"] = pd.to_numeric(
        customers["age"],
        errors="coerce",
    )

    customers["age"] = customers["age"].fillna(
        customers["age"].median()
    )

    customers["age"] = (
        customers["age"]
        .clip(18, 100)
        .astype(int)
    )

    return customers



# Clean Products


def clean_products(products):

    products = products.copy()

    products["unit_price"] = pd.to_numeric(
        products["unit_price"],
        errors="coerce",
    )

    products["cost_price"] = pd.to_numeric(
        products["cost_price"],
        errors="coerce",
    )

    products["stock_quantity"] = pd.to_numeric(
        products["stock_quantity"],
        errors="coerce",
    )

    products["unit_price"] = (
        products["unit_price"]
        .fillna(products["unit_price"].median())
        .clip(lower=0)
    )

    products["cost_price"] = (
        products["cost_price"]
        .fillna(products["cost_price"].median())
        .clip(lower=0)
    )

    products["stock_quantity"] = (
        products["stock_quantity"]
        .fillna(0)
        .clip(lower=0)
        .astype(int)
    )

    return products



# Clean Orders


def clean_orders(orders):

    orders = orders.copy()

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce",
    )

    orders["shipping_date"] = pd.to_datetime(
        orders["shipping_date"],
        errors="coerce",
    )

    orders["delivery_date"] = pd.to_datetime(
        orders["delivery_date"],
        errors="coerce",
    )

    orders = orders.dropna(
        subset=[
            "order_id",
            "customer_id",
            "order_date",
        ]
    )

    orders = orders.drop_duplicates(
        subset=["order_id"],
        keep="first",
    )

    orders["order_status"] = (
        orders["order_status"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    orders["payment_method"] = (
        orders["payment_method"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    return orders



# Clean Order Items


def clean_order_items(order_items):

    order_items = order_items.copy()

    order_items["quantity"] = pd.to_numeric(
        order_items["quantity"],
        errors="coerce",
    )

    order_items["unit_price"] = pd.to_numeric(
        order_items["unit_price"],
        errors="coerce",
    )

    order_items["discount_percent"] = pd.to_numeric(
        order_items["discount_percent"],
        errors="coerce",
    )

    order_items = order_items.dropna(
        subset=[
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
        ]
    )

    order_items = order_items[
        order_items["quantity"] > 0
    ]

    order_items["discount_percent"] = (
        order_items["discount_percent"]
        .fillna(0)
        .clip(0, 100)
    )

    order_items["gross_amount"] = (
        order_items["quantity"]
        * order_items["unit_price"]
    )

    order_items["discount_amount"] = (
        order_items["gross_amount"]
        * order_items["discount_percent"]
        / 100
    )

    order_items["net_amount"] = (
        order_items["gross_amount"]
        - order_items["discount_amount"]
    )

    return order_items



# Feature Engineering


def build_order_level_dataset(
    orders,
    order_items,
    customers,
):

    order_values = (
        order_items
        .groupby("order_id", as_index=False)
        .agg(
            order_revenue=("net_amount", "sum"),
            total_items=("quantity", "sum"),
            total_discount=("discount_amount", "sum"),
        )
    )

    order_df = orders.merge(
        order_values,
        on="order_id",
        how="left",
    )

    order_df = order_df.merge(
        customers[
            [
                "customer_id",
                "customer_segment",
                "city",
                "age",
                "gender",
            ]
        ],
        on="customer_id",
        how="left",
    )

    order_df["order_revenue"] = (
        order_df["order_revenue"]
        .fillna(0)
    )

    order_df["total_items"] = (
        order_df["total_items"]
        .fillna(0)
        .astype(int)
    )

    order_df["total_discount"] = (
        order_df["total_discount"]
        .fillna(0)
    )

    order_df["order_month"] = (
        order_df["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    order_df["order_year"] = (
        order_df["order_date"]
        .dt.year
    )

    order_df["order_week"] = (
        order_df["order_date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    order_df["order_day"] = (
        order_df["order_date"]
        .dt.day_name()
    )

    order_df["is_weekend"] = (
        order_df["order_date"]
        .dt.dayofweek >= 5
    )

    order_df["shipping_days"] = (
        order_df["shipping_date"]
        - order_df["order_date"]
    ).dt.days

    order_df["delivery_days"] = (
        order_df["delivery_date"]
        - order_df["order_date"]
    ).dt.days

    order_df["shipping_days"] = (
        order_df["shipping_days"]
        .clip(lower=0)
    )

    order_df["delivery_days"] = (
        order_df["delivery_days"]
        .clip(lower=0)
    )

    return order_df



# Customer-Level Features


def build_customer_features(
    order_df,
    customers,
):

    completed = order_df[
        order_df["order_status"] == "Completed"
    ].copy()

    customer_features = (
        completed
        .groupby("customer_id")
        .agg(
            total_orders=(
                "order_id",
                "nunique",
            ),
            total_revenue=(
                "order_revenue",
                "sum",
            ),
            average_order_value=(
                "order_revenue",
                "mean",
            ),
            total_items=(
                "total_items",
                "sum",
            ),
            last_purchase_date=(
                "order_date",
                "max",
            ),
            first_purchase_date=(
                "order_date",
                "min",
            ),
        )
        .reset_index()
    )

    analysis_date = (
        order_df["order_date"].max()
        + pd.Timedelta(days=1)
    )

    customer_features[
        "days_since_last_purchase"
    ] = (
        analysis_date
        - customer_features["last_purchase_date"]
    ).dt.days

    customer_features[
        "customer_lifetime_value_proxy"
    ] = (
        customer_features["total_revenue"]
    )

    customer_features[
        "purchase_lifetime_days"
    ] = (
        customer_features["last_purchase_date"]
        - customer_features["first_purchase_date"]
    ).dt.days

    customer_features[
        "purchase_lifetime_days"
    ] = customer_features[
        "purchase_lifetime_days"
    ].clip(lower=1)

    customer_features[
        "revenue_per_day_active"
    ] = (
        customer_features["total_revenue"]
        / customer_features["purchase_lifetime_days"]
    )

    customer_features = customers.merge(
        customer_features,
        on="customer_id",
        how="left",
    )

    numeric_columns = [
        "total_orders",
        "total_revenue",
        "average_order_value",
        "total_items",
        "days_since_last_purchase",
        "customer_lifetime_value_proxy",
        "purchase_lifetime_days",
        "revenue_per_day_active",
    ]

    customer_features[numeric_columns] = (
        customer_features[numeric_columns]
        .fillna(0)
    )

    # 90-day inactivity rule.
    customer_features["churn_risk"] = np.select(
        [
            customer_features[
                "days_since_last_purchase"
            ] >= 180,

            customer_features[
                "days_since_last_purchase"
            ] >= 90,

            customer_features[
                "days_since_last_purchase"
            ] >= 60,
        ],
        [
            "High Risk",
            "At Risk",
            "Watch",
        ],
        default="Active",
    )

    return customer_features



# Validation


def validate_data(
    customers,
    products,
    orders,
    order_items,
):

    assert customers["customer_id"].notna().all()
    assert products["product_id"].notna().all()
    assert orders["order_id"].notna().all()

    assert (
        order_items["quantity"] > 0
    ).all()

    assert (
        order_items["discount_percent"]
        .between(0, 100)
        .all()
    )

    assert (
        order_df_revenue_check(order_items)
    )

    print("\nValidation passed.")


def order_df_revenue_check(order_items):

    return (
        order_items["net_amount"]
        >= 0
    ).all()



# Main ETL


def main():

    print("Loading raw datasets...")

    (
        customers,
        products,
        orders,
        order_items,
        payments,
    ) = load_data()

    print("Cleaning customers...")
    customers = clean_customers(
        customers
    )

    print("Cleaning products...")
    products = clean_products(
        products
    )

    print("Cleaning orders...")
    orders = clean_orders(
        orders
    )

    print("Cleaning order items...")
    order_items = clean_order_items(
        order_items
    )

    print("Building order-level dataset...")

    order_df = build_order_level_dataset(
        orders,
        order_items,
        customers,
    )

    print("Building customer features...")

    customer_features = build_customer_features(
        order_df,
        customers,
    )

    print("Validating datasets...")

    validate_data(
        customers,
        products,
        orders,
        order_items,
    )

    # Save processed datasets.

    order_df.to_csv(
        PROCESSED_DIR / "orders_clean.csv",
        index=False,
    )

    customer_features.to_csv(
        PROCESSED_DIR / "customers_features.csv",
        index=False,
    )

    print("\nETL completed successfully.")

    print(
        f"Processed orders: "
        f"{len(order_df):,}"
    )

    print(
        f"Customer features: "
        f"{len(customer_features):,}"
    )


if __name__ == "__main__":
    main()