import requests
import os, json

def inserir_novos_urls_json(arquivo_caminho, novos_dados):
    # Lista para armazenar os URLs existentes
    urls_existentes = set()

    # Carrega o conteúdo existente, se o arquivo existir
    if os.path.exists(arquivo_caminho):
        with open(arquivo_caminho, 'r', encoding='utf-8') as arquivo:
            try:
                conteudo_atual = json.load(arquivo)
                urls_existentes = {item['url'] for item in conteudo_atual}
            except json.JSONDecodeError:
                print("O arquivo existente não contém um JSON válido.")
                conteudo_atual = []
    else:
        conteudo_atual = []

    # Filtra os novos dados para incluir apenas URLs não existentes
    novos_registros = [
        item for item in novos_dados if item['url'] not in urls_existentes
    ]

    # Verifica se há novos registros a serem inseridos
    if novos_registros:
        conteudo_atual.extend(novos_registros)
        # Salva o conteúdo atualizado no arquivo
        with open(arquivo_caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(conteudo_atual, arquivo, indent=4, ensure_ascii=False)
        print(f"{len(novos_registros)} novos registros inseridos.")
    else:
        print("Nenhum novo registro para inserir.")

def get_news(search_params):

    # my_key = "be9b7ceffe094a30a802a4b1961a5839"

    url = "https://newsapi.org/v2/everything"
    # params = {
    #     "q": "Energy Minerals Market",
    #     "from": "2025-01-19",
    #     "apiKey": my_key
    # }

    result = requests.get(url, params=search_params)

    return result.json()['articles']

# inserir_novos_urls("dayly_news.json", result.json()['articles'])