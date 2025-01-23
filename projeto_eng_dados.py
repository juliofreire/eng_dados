from pyspark.sql import SparkSession

# Cria a SparkSession
spark = SparkSession.builder.master("spark://172.22.36.44:7077").appName("Test PySpark Script").getOrCreate()

# Testa a criação de um DataFrame simples
data = [("John", 25), ("Alice", 30), ("Bob", 35)]
columns = ["Name", "Age"]

df = spark.createDataFrame(data, columns)

# Exibe o DataFrame
df.show()

# Parando a SparkSession
spark.stop()
