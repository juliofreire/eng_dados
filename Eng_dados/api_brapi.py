import requests


def get_stocks(search_params):

    my_token = "4zun5s1j59wx9tuFnLt6zn"

    url = "https://brapi.dev/api/quote/list"
    # params = {
    #     'sortBy': 'close',
    #     'sortOrder': 'desc',
    #     'limit': '10',
    #     'sector': 'Energy Minerals',
    #     'type': 'stock',
    #     'token': my_token,
    # }
    response = requests.get(url, params=search_params)

    res = response.json()

    return res['stocks']

# for stock in res["stocks"]:
#     inserir_arqv(cliente, 'db_eng_dados', 'acoes', stock)

# print(response.json())