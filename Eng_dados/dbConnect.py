from pymongo import MongoClient


def conectar_mongo():
    # client = MongoClient("mongodb://localhost:27017")
    # client = MongoClient("mongodb://root:example@mongodb:27017/replicaSet=primary")
    cmd = "mongodb://root:example@127.0.0.1:27017/?authSource=admin&directConnection=true"
    client = MongoClient(cmd)
    print("ainda estou aqui")


    return client

def inserir_arqv(cliente, nome_db, nome_colecao, documento, pk="stock"):
    # Seleciona o banco de dados e a coleção
    db = cliente[nome_db]
    colecao = db[nome_colecao]

    # Verifica se o documento já existe
    resultado = encontrar_arqv(cliente, nome_db, nome_colecao, documento[pk], pk)

    if resultado:
        colecao.find_one_and_update({pk: documento[pk]}, {"$set": documento})
        print("Arquivo Atualizado")
        return

    # Tenta inserir o documento
    try:
        colecao.insert_one(documento)
        print("Arquivo inserido com sucesso")
    except Exception as err:
        print(f"Erro ao inserir arquivo: \n\t {err}")


def encontrar_arqv(cliente, nome_db, nome_colecao, valor_pk, pk="stock"):
    # Seleciona o banco de dados e a coleção
    db = cliente[nome_db]
    colecao = db[nome_colecao]

    try:
        # Busca o documento com o filtro
        resultado = colecao.find_one({pk: valor_pk})
        return resultado
    except Exception as err:
        print(f"Erro ao buscar arquivo: \n\t {err}")
        return None


