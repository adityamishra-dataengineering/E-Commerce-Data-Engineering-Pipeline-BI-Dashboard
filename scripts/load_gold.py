import os
from pyspark.sql import SparkSession

# Fetch database credentials securely from environment variables
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "olist_warehouse")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-db")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

if not MYSQL_PASSWORD:
    raise ValueError("❌ MYSQL_ROOT_PASSWORD environment variable is not set!")

# Build dynamic JDBC URL
jdbc_url = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
connection_props = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Initialize Spark Session using the local JAR driver
spark = SparkSession.builder \
    .appName("ExportGoldToCSV") \
    .config("spark.jars", "/app/mysql-connector-java-8.0.28.jar") \
    .getOrCreate()

# Gold layer tables
tables = ["fact_sales", "dim_customers", "dim_products", "dim_sellers", "dim_time"]

for table in tables:
    print(f"Exporting {table} from MySQL...")
    try:
        df = spark.read.jdbc(url=jdbc_url, table=table, properties=connection_props)
        
        # Save as CSV in the mounted /app container path
        df.coalesce(1).write \
          .mode("overwrite") \
          .option("header", "true") \
          .csv(f"/app/data/gold_csv/{table}")
        print(f" Successfully exported {table}")
    except Exception as e:
        print(f"❌ Failed to export {table}: {e}")

print(" All Gold tables processed!")
spark.stop()