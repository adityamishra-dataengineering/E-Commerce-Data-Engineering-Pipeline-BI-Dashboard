import os
from pyspark.sql import SparkSession

def init_spark():
    return SparkSession.builder \
        .appName("Olist-MySQL-Loader") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

if __name__ == "__main__":
    GOLD_DIR = "/app/data/gold"
    
    # Securely retrieve credentials from environment variables
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")  # Fetch from container env
    
    if not MYSQL_PASSWORD:
        raise ValueError("❌ MYSQL_ROOT_PASSWORD environment variable is not set!")

    spark = init_spark()
    print("🔄 Exporting Gold Tables to MySQL Production Warehouse...")
    
    jdbc_url = "jdbc:mysql://mysql-db:3306/olist_dw?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true"
    properties = {
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    
    gold_tables = ["dim_customers", "dim_products", "dim_sellers", "dim_time", "fact_sales"]
    
    for table in gold_tables:
        print(f"🚀 Loading table {table} to MySQL...")
        df = spark.read.parquet(os.path.join(GOLD_DIR, table))
        
        df.write.jdbc(
            url=jdbc_url,
            table=table,
            mode="overwrite",
            properties=properties
        )
        print(f"✅ {table} loaded successfully.")
        
    print("🎉 All Gold tables successfully written to MySQL!")
    spark.stop()