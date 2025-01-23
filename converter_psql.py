from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, MapType
import json

# Cria a SparkSession
spark = SparkSession.builder \
    .master("spark://172.22.36.44:7077") \
    .appName("Processar Payloads") \
    .getOrCreate()

# Define o caminho do arquivo
file_path = "arquivo.txt"

# Lê o arquivo como DataFrame (JSON por linha)
data = spark.read.text(file_path)

# Define o schema do JSON para o campo "payload"
payload_schema = StringType()

# Extraindo apenas o payload do JSON
payloads = data.select(from_json(col("value"), MapType(StringType(), StringType())).alias("json")) \
               .select(col("json.payload").alias("payload"))

# Mostra os payloads extraídos (opcional para validação)
#payloads.show(truncate=False)

# Define a função para processar cada payload
def converter_mg2pg(obj_mongo):
    ignored_atributes = ['_id', 'logo']
    res = []

    # Garante que obj_mongo seja um dicionário JSON
    if isinstance(obj_mongo, str):
        obj_mongo = json.loads(obj_mongo)

    # Verifica se o objeto tem a chave 'after' e a processa
    if 'after' in obj_mongo and obj_mongo['after']:
        # Converte o campo 'after' (string JSON) para um dicionário Python
        obj_mongo = json.loads(obj_mongo['after'])
    else:
        # Caso 'after' seja None ou não exista, retorna uma tupla vazia
        return tuple(res)

    # Lógica de conversão do campo 'type'
    if obj_mongo['type'] == 'stock':
        obj_mongo['type'] = 1
    elif obj_mongo['type'] == 'fund':
        obj_mongo['type'] = 2
    elif obj_mongo['type'] == 'bdr':
        obj_mongo['type'] = 3

    # Adiciona os atributos ao resultado, ignorando os especificados
    for atribute in obj_mongo:
        if atribute not in ignored_atributes:
            value = obj_mongo[atribute]

            # Verifica se o valor é um dicionário com a chave "$numberLong"
            if isinstance(value, dict) and "$numberLong" in value:
                value = int(value["$numberLong"])  # Converte o valor para inteiro

            res.append(value)
            
    return tuple(res)

def process_payload(row):
    payload = row["payload"]
    if payload != None:
        obj_postgre = converter_mg2pg(json.loads(payload))
        print(f"Objeto Convertido: {obj_postgre}")
        # print(f"Tipo do objeto: {type(payload)}")

# Converte para RDD e executa o processamento em cada worker
payloads.rdd.foreach(process_payload)

# Finaliza a SparkSession
spark.stop()