import requests
import base64
import json

# URL do endpoint GraphQL
url = "https://www.bemolfarma.com.br/_v/segment/graphql/v1"

# Decodificando as variáveis
encoded_variables = "eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6dHJ1ZSwic2t1c0ZpbHRlciI6IkFMTF9BVkFJTEFCTEUiLCJpbnN0YWxsbWVudENyaXRlcmlhIjoiTUFYX1dJVEhPVVRfSU5URVJFU1QiLCJjYXRlZ29yeSI6IiIsImNvbGxlY3Rpb24iOiIxMzgiLCJzcGVjaWZpY2F0aW9uRmlsdGVycyI6WyJzcGVjaWZpY2F0aW9uRmlsdGVyX1RhcmphIGRvIE1lZGljYW1lbnRvOlZlbmRhIExpdnJlIl0sIm9yZGVyQnkiOiIiLCJmcm9tIjowLCJ0byI6MTUsInNoaXBwaW5nT3B0aW9ucyI6W10sInZhcmlhbnQiOiIiLCJhZHZlcnRpc2VtZW50T3B0aW9ucyI6eyJzaG93U3BvbnNvcmVkIjpmYWxzZSwic3BvbnNvcmVkQ291bnQiOjIsInJlcGVhdFNwb25zb3JlZFByb2R1Y3RzIjpmYWxzZSwiYWR2ZXJ0aXNlbWVudFBsYWNlbWVudCI6ImhvbWVfc2hlbGYifX0="
variables = json.loads(base64.b64decode(encoded_variables).decode('utf-8'))

# Corpo da requisição GraphQL
payload = {
    "operationName": "Products",
    "variables": variables,
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "21326beabc3e4114a48f876e981ac6f0c1561482d9ef2b773c08b8b57e2f83d6",
            "sender": "vtex.store-resources@0.x",
            "provider": "vtex.search-graphql@0.x"
        }
    }
}

# Cabeçalhos adicionais para a requisição
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Enviando a requisição e verificando a resposta
response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    try:
        response_data = response.json()

        # Verificar o tipo da resposta e imprimir para debug
        if isinstance(response_data, list):
            print("Resposta é uma lista. Conteúdo da resposta:", response_data)
        elif isinstance(response_data, dict):
            # Aqui você deve verificar a estrutura específica que foi retornada
            print("Resposta é um dicionário. Conteúdo da resposta:", response_data)
            data = response_data.get('data', {}).get('products', {}).get('edges', [])
            for product in data:
                name = product.get('node', {}).get('name', 'Nome não encontrado')
                price = product.get('node', {}).get('price', {}).get('sellingPrice', 'Preço não encontrado')
                print(f"Nome: {name}\nPreço: {price}\n{'-' * 40}")
        else:
            print("A resposta não é nem lista nem dicionário. Conteúdo:", response_data)
    except ValueError as e:
        print(f"Erro ao analisar o JSON: {e}")
else:
    print(f"Erro: {response.status_code}")
