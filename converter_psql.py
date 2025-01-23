from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, MapType
import json

import psycopg2

def conectar_postgre():
    conn = None
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname='db_eng_dados',
            user='root',
            password='example',
            host='localhost',
            port='5432'  # porta padrão do PostgreSQL
        )
        print("Conexao bem sucedida")
        return conn
    except Exception as err:
        print(f"Erro ao conectar no postegree {err}" )

def consulta_postgresql(conn, query_consulta):
    try:
        # Criando um cursor
        cursor = conn.cursor()
        
        # Executando uma consulta
        cursor.execute(query_consulta)
        
        # Recuperando os resultados
        resultados = cursor.fetchall()
        
        # Imprimindo os resultados
        # for row in resultados:
        #     print(row)
        
        # Fechando o cursor
        cursor.close()
        return resultados

    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def inserir_postgre(conn, insert_query):
    cursor = conn.cursor()

    try:
        cursor.execute(insert_query)
        conn.commit()
        print("Dados inseridos!")
    except Exception as err:
        print(f"Erro ao inserir dados {err}")

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
    cliente_postgre = conectar_postgre()
    query = ''

    payload = row["payload"]
    if payload != None:
        payload_json = json.loads(json.loads(payload)['after'])
        obj_postgre = converter_mg2pg(json.loads(payload))
        print(payload_json)
        print(f'TIPO DO PAY{type(payload_json)}')

        dado_inserido = consulta_postgresql(cliente_postgre, f"SELECT * FROM stocks WHERE stock= '{payload_json['stock']}'")
        if dado_inserido:
            # Verifica se o valor é um dicionário com a chave "$numberLong"
            if isinstance(payload_json['market_cap'], dict) and "$numberLong" in payload_json['market_cap']:
                payload_json['market_cap'] = int(payload_json['market_cap']["$numberLong"])
            query = f"UPDATE stocks SET close = {payload_json['close']}, change = {payload_json['change']}, volume = {payload_json['volume']}, market_cap = {payload_json['market_cap']}"
            print("O dado será atualizado")
        else:
             query = f"INSERT INTO stocks (stock, name, close, change, volume, market_cap, sector, stock_type_id) VALUES {obj_postgre}"
        inserir_postgre(cliente_postgre, query)

# Converte para RDD e executa o processamento em cada worker
payloads.rdd.foreach(process_payload)

# Finaliza a SparkSession
spark.stop()