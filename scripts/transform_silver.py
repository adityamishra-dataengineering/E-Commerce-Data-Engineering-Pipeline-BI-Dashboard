import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, coalesce, lit, when

def init_spark():
    return SparkSession.builder \
        .appName("Olist-Silver-Transformation") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

def clean_orders(spark, bronze_dir, silver_dir):
    print("🔄 Processing Silver: Orders...")
    df = spark.read.parquet(os.path.join(bronze_dir, "olist_orders_dataset"))
    
    date_cols = [
        "order_purchase_timestamp", "order_approved_at", 
        "order_delivered_carrier_date", "order_delivered_customer_date", 
        "order_estimated_delivery_date"
    ]
    for c in date_cols:
        df = df.withColumn(c, to_timestamp(col(c), "yyyy-MM-dd HH:mm:ss"))
        
    df = df.withColumn("order_status", coalesce(col("order_status"), lit("unknown")))
    df = df.dropDuplicates(["order_id"])
    
    df.write.mode("overwrite").parquet(os.path.join(silver_dir, "olist_orders_dataset"))
    print("✅ Silver Orders Complete.")

def clean_customers(spark, bronze_dir, silver_dir):
    print("🔄 Processing Silver: Customers...")
    df = spark.read.parquet(os.path.join(bronze_dir, "olist_customers_dataset"))
    df = df.dropDuplicates(["customer_id"])
    df.write.mode("overwrite").parquet(os.path.join(silver_dir, "olist_customers_dataset"))
    print("✅ Silver Customers Complete.")

def clean_order_items(spark, bronze_dir, silver_dir):
    print("🔄 Processing Silver: Order Items...")
    df = spark.read.parquet(os.path.join(bronze_dir, "olist_order_items_dataset"))
    df = df.withColumn("shipping_limit_date", to_timestamp(col("shipping_limit_date"), "yyyy-MM-dd HH:mm:ss"))
    df = df.withColumn("price", when(col("price") < 0, 0.0).otherwise(col("price")))
    df = df.withColumn("freight_value", when(col("freight_value") < 0, 0.0).otherwise(col("freight_value")))
    
    df.write.mode("overwrite").parquet(os.path.join(silver_dir, "olist_order_items_dataset"))
    print("✅ Silver Order Items Complete.")

def clean_products(spark, bronze_dir, silver_dir):
    print("🔄 Processing Silver: Products...")
    df = spark.read.parquet(os.path.join(bronze_dir, "olist_products_dataset"))
    df = df.dropDuplicates(["product_id"])
    df.write.mode("overwrite").parquet(os.path.join(silver_dir, "olist_products_dataset"))
    print("✅ Silver Products Complete.")

if __name__ == "__main__":
    BASE_DIR = "/app" 
    BRONZE_DIR = os.path.join(BASE_DIR, "data", "bronze")
    SILVER_DIR = os.path.join(BASE_DIR, "data", "silver")
    
    spark_session = init_spark()
    
    clean_orders(spark_session, BRONZE_DIR, SILVER_DIR)
    clean_customers(spark_session, BRONZE_DIR, SILVER_DIR)
    clean_order_items(spark_session, BRONZE_DIR, SILVER_DIR)
    clean_products(spark_session, BRONZE_DIR, SILVER_DIR)
    
    spark_session.stop()