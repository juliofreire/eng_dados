from dbConnect import *
from api_brapi import *
from api_news import *
import datetime

cliente = conectar_mongo()


themes_array = ['Energy Minerals', 'Transportation', 'Non-Energy Minerals', 'Technology Services', 'Health Technology']
search_params_stocks = {
    'sortBy': 'close',
    'sortOrder': 'desc',
    'limit': '10',
    'sector': '',
    'type': 'stock',
    'token': "4zun5s1j59wx9tuFnLt6zn"
}


search_params_news = {
    "q": "",
    "from": '2025-01-20',
    "apiKey": "be9b7ceffe094a30a802a4b1961a5839"
}

for theme in themes_array:
    search_params_stocks['sector'] = theme
    search_params_news['q'] = theme + " Market"
    stocks = get_stocks(search_params_stocks)
    for stock in stocks:
        inserir_arqv(cliente, 'db_eng_dados', 'acoes', stock)
    news = get_news(search_params_news)
    inserir_novos_urls_json('dayly_news.json', news)


