# E-Commerce Exploratory Data Analysis & Sales Pipeline

An end-to-end e-commerce analytics project demonstrating **Python data generation, PostgreSQL database management, SQL analytics, Pandas ETL, feature engineering, customer segmentation, and business-focused exploratory data analysis**.

---

## 📌 Project Overview

This project simulates an e-commerce business and builds a complete analytics workflow from **raw transactional data to actionable business insights**.

### Tech Stack

* Python
* Pandas
* NumPy
* PostgreSQL
* SQLAlchemy
* SQL
* Matplotlib
* Seaborn
* Jupyter Notebook

---

## 🏗️ Project Architecture

```text
                Python
                  │
                  ▼
          Data Generation
                  │
                  ▼
             Raw CSV Data
                  │
                  ▼
             PostgreSQL
                  │
          ┌───────┴────────┐
          ▼                ▼
     SQL Analytics      Pandas ETL
          │                │
          │                ▼
          │        Feature Engineering
          │                │
          └───────┬────────┘
                  ▼
          Jupyter Notebook
                  │
                  ▼
          EDA & Visualization
                  │
                  ▼
          Business Insights
```

---

## 📊 Dataset

The synthetic dataset contains:

| Dataset     |                 Records |
| ----------- | ----------------------: |
| Customers   |                   5,000 |
| Products    |                     300 |
| Orders      |                  20,000 |
| Order Items | Multi-item transactions |
| Payments    |         Payment history |

### Realistic Data Quality Scenarios

* Duplicate customer records
* Missing city values
* Missing shipping & delivery dates
* Cancelled and returned orders
* Failed & pending payments
* Skewed order values
* Variable discounts
* Uneven customer purchase frequency

---

## 🗄️ Database Schema

The project uses a normalized PostgreSQL database with five tables:

* **customers** – Customer demographic & registration data
* **products** – Product catalog, pricing & inventory
* **orders** – Order lifecycle & transactions
* **order_items** – Products purchased per order
* **payments** – Payment methods & statuses

---

## 🔎 SQL Analytics

### Window Functions

* Rolling revenue analysis
* Customer order ranking
* Month-over-month revenue growth

### Common Table Expressions (CTEs)

* Cohort analysis
* Customer retention
* Purchasing behavior
* Multi-step business queries

### RFM Segmentation

Customers are scored using:

* **Recency**
* **Frequency**
* **Monetary Value**

NTILE-based scoring is used to classify customer segments.

---

## 🔄 Pandas ETL Pipeline

`etl.py` performs:

* Schema validation
* Duplicate removal
* Datetime conversion
* Numeric type conversion
* Missing-value treatment
* Invalid-value filtering
* Order aggregation
* Customer aggregation
* Data validation

Processed datasets are stored in:

```text
data/processed/
```

---

## ⚙️ Feature Engineering

| Feature                         | Formula                       |
| ------------------------------- | ----------------------------- |
| Average Order Value             | Total Revenue ÷ Orders        |
| Days Since Last Purchase        | Analysis Date − Last Purchase |
| Customer Lifetime Value (Proxy) | Historical Customer Revenue   |
| Shipping Days                   | Shipping Date − Order Date    |
| Delivery Days                   | Delivery Date − Order Date    |

---

## 👥 Customer Risk Segmentation

Customers are classified using purchase inactivity.

| Segment      | Criteria                   |
| ------------ | -------------------------- |
| 🟢 Active    | Recent purchasing activity |
| 🟡 Watch     | 60+ days inactive          |
| 🟠 At Risk   | 90+ days inactive          |
| 🔴 High Risk | 180+ days inactive         |

> **Note:** This is a rule-based churn-risk classification, not a machine learning model.

---

## 📈 Exploratory Data Analysis

The notebook **`notebooks/01_ecommerce_analysis.ipynb`** includes:

### Business KPIs

* Total Revenue
* Completed Orders
* Average Order Value
* Total Customers

### Revenue Analysis

* Monthly revenue trend
* Monthly order volume

### Customer Analysis

* Top customers
* Revenue by customer segment

### Churn Analysis

* Customer risk distribution
* Revenue by risk group

### Category Analysis

* Revenue by product category
* Items sold by category

### Delivery Analysis

* Shipping & delivery performance

---

## 💼 Business Questions Answered

* How much revenue is generated from completed orders?
* How does revenue change over time?
* Which customer segments contribute the most revenue?
* Who are the highest-value customers?
* Which customers are at risk of churn?
* Which product categories perform best?
* How efficient is the delivery process?

---

## 📁 Project Structure

```text
ecommerce-eda-sales-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 01_ecommerce_analysis.ipynb
│
├── outputs/
│   └── figures/
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_data_quality.sql
│   ├── 03_sales_analysis.sql
│   ├── 04_customer_analysis.sql
│   ├── 05_cohort_retention.sql
│   └── 06_rfm_segmentation.sql
│
├── src/
│   ├── make_data.py
│   ├── load_db.py
│   ├── etl.py
│   └── __init__.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run_pipeline.py
```

---

## 🚀 How to Run

### 1. Clone Repository

```bash
git clone https://github.com/Shad0wcoder/ecommerce-eda-sales-pipeline.git
cd ecommerce-eda-sales-pipeline
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate (Windows):

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/ecommerce
```

### 5. Run Pipeline

```bash
python run_pipeline.py
```

Pipeline execution:

```text
Data Generation
      ↓
PostgreSQL Loading
      ↓
ETL & Feature Engineering
```

### 6. Run EDA Notebook

```bash
jupyter notebook
```

Open:

```text
notebooks/01_ecommerce_analysis.ipynb
```

---

## 📤 Outputs

| Folder             | Description                   |
| ------------------ | ----------------------------- |
| `data/processed/`  | Cleaned & engineered datasets |
| `outputs/figures/` | EDA visualizations            |

---

## 🎯 Key Skills Demonstrated

* Python
* PostgreSQL
* SQL
* Pandas
* NumPy
* SQLAlchemy
* ETL Pipeline Development
* Data Cleaning
* Feature Engineering
* Exploratory Data Analysis
* Data Visualization
* Customer Segmentation
* RFM Analysis
* Cohort Analysis
* Business Analytics

---

## 📌 Conclusion

This project demonstrates a complete data analytics workflow—from synthetic data generation and relational database modeling to SQL analytics, ETL, exploratory analysis, visualization, and business insights. It is designed to showcase practical skills required for **Data Analyst** and **entry-level Data Science** roles.

---

## 👤 Author

**Rohit Vishwakarma**

GitHub: **[@Shad0wcoder](https://github.com/Shad0wcoder)**
