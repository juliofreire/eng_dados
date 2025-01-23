import psycopg2

def conectar_postgre():
    conn = None
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(
            dbname='db_eng_dados',
            user='postgres',
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
