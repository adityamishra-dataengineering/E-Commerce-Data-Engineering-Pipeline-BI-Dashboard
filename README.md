# 🛒 E-Commerce Data Engineering Pipeline & BI Dashboard

A containerized, end-to-end data engineering pipeline that processes the Brazilian Olist E-Commerce dataset (~100k orders). It implements a **Medallion Architecture** (Bronze → Silver → Gold) to turn raw CSV files into a production-style **Star Schema** data warehouse using **PySpark**, **Apache Airflow**, **MySQL**, **Streamlit**, and **Tableau**.

📊 **Live dashboard:** [View the Tableau Public dashboard](https://public.tableau.com/views/Book1_17889684359940/Dashboard1)

---

## 📌 Architecture & Pipeline Flow

```text
Raw Olist CSVs (Kaggle)
        │
        ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Bronze Layer   │──▶│  Silver Layer   │──▶│   Gold Layer    │
│  Raw Parquet    │   │  Cleaned &      │   │   Star Schema   │
│                 │   │  Deduplicated   │   │   Parquet       │
└─────────────────┘   └─────────────────┘   └────────┬────────┘
                                                     │ JDBC
                                                     ▼
                                            ┌─────────────────┐
                                            │  MySQL Data     │
                                            │  Warehouse      │
                                            └────────┬────────┘
                                         ┌───────────┴───────────┐
                                         ▼                       ▼
                                ┌─────────────────┐     ┌─────────────────┐
                                │  Streamlit App  │     │  Tableau BI     │
                                │  (Control/Ops)  │     │  Dashboard      │
                                └─────────────────┘     └─────────────────┘
```

Airflow orchestrates the four PySpark steps in order and handles retries.

### Transformation Breakdown

1. **Bronze (raw storage):** Ingests the multi-table CSVs with PySpark and writes them to Parquet, preserving the raw schemas.
2. **Silver (cleansing & normalization):** Data type casting, null handling, duplicate removal, and canceled-order filtering.
3. **Gold (dimensional modeling):** Models the cleaned data into a **Star Schema**: `fact_sales` surrounded by dimension tables for customers, products, sellers, and time.
4. **Warehouse export:** Loads the Gold tables into **MySQL** via JDBC.
5. **Analytics & monitoring:**
   * **Streamlit web UI:** Interactive app for job status tracking and local data exploration.
   * **Tableau Public dashboard:** BI dashboard covering **$16.57M+** in processed sales. [Open it here](https://public.tableau.com/views/Book1_17889684359940/Dashboard1).

---

## 🧠 Key Design Decisions

* **Medallion Architecture:** Separates raw, cleaned, and modeled data so each stage can be debugged and re-run independently.
* **Parquet storage:** Columnar and compressed, which makes Spark reads and writes much faster than CSV and preserves schemas.
* **Star Schema in the Gold layer:** Simple joins and fast aggregations for BI tools like Tableau.
* **Airflow for orchestration:** Explicit task dependencies, scheduling, and automatic retries instead of running scripts by hand.
* **Docker Compose:** The whole stack starts with one command and runs the same on any machine.

---

## 🛠️ Tech Stack

* **Languages:** Python, SQL
* **Processing:** Apache Spark (PySpark)
* **Orchestration:** Apache Airflow
* **Data Warehouse:** MySQL
* **Storage Format:** Apache Parquet
* **UI & Analytics:** Streamlit, Tableau Public
* **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

```text
olist-data-pipeline/
│
├── app/                      # Web interface
│   ├── assets/               # UI images, architecture diagrams, screenshots
│   └── main.py               # Streamlit application
│
├── dags/
│   └── olist_pipeline_dag.py # Airflow DAG defining the task chain
│
├── data/                     # Local data lake (Git-ignored)
│   ├── raw/                  # Source Kaggle CSV files
│   ├── bronze/               # Raw Parquet files
│   ├── silver/               # Cleaned Parquet files
│   └── gold/                 # Fact & dimension Parquet files
│
├── scripts/
│   ├── ingest_bronze.py      # Step 1: Raw CSV -> Bronze Parquet
│   ├── transform_silver.py   # Step 2: Bronze -> Clean Silver Parquet
│   ├── load_gold.py          # Step 3: Silver -> Star Schema Gold Parquet
│   └── load_to_mysql.py      # Step 4: Gold Parquet -> MySQL warehouse
│
├── docker-compose.yml        # Provisions Airflow, Spark, and MySQL
├── .env.example              # Template for environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Setup & Execution

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
* Olist dataset CSVs from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), placed in `data/raw/`

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd olist-data-pipeline
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your own database credentials.

3. **Start the containers**
   ```bash
   docker-compose up -d
   ```

4. **Trigger the pipeline in Airflow**
   * Open `http://localhost:8080` and log in with the credentials set in your compose file.
   * Unpause and trigger the `olist_ecommerce_data_pipeline` DAG.

5. **Launch the Streamlit app**
   ```bash
   pip install -r requirements.txt
   streamlit run app/main.py
   ```

6. **Verify the MySQL warehouse**
   ```bash
   docker exec -it mysql-db mysql -u root -p olist_dw -e "SHOW TABLES;"
   ```

---

## 🔒 Security & Best Practices

* **Environment isolation:** Credentials (`.env`), logs, and local Parquet storage (`data/`) are excluded from Git via `.gitignore`. Only `.env.example` with placeholders is committed.
* **Modular design:** Ingestion, cleaning, modeling, and loading live in separate PySpark scripts.
* **Orchestration resilience:** Airflow manages dependencies, scheduling, and task retries.

---

## 🔭 Future Improvements

* Add data quality checks (e.g., Great Expectations) between layers
* Add incremental loads instead of full refreshes
* Add CI with linting and DAG validation

---

## 👨‍💻 Author

**Aditya Mishra**
Final-year B.Tech Computer Science student at SRMU | Aspiring Data Engineer

* LinkedIn:(https://www.linkedin.com/in/adityamishra-dataeng/)
* GitHub:(https://github.com/adityamishra-dataengineering)