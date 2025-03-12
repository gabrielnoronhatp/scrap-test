import requests
import json

def buscar_produtos_paginados(pagina, produtos_por_pagina=100):
    # Calcular os valores de `from` e `to`
    from_index = (pagina - 1) * produtos_por_pagina
    to_index = from_index + produtos_por_pagina - 1
    
    # URL do endpoint GraphQL
    url = "https://www.bemolfarma.com.br/_v/segment/graphql/v1"
    
    # Preparar as variáveis para a consulta
    variables = {
        "hideUnavailableItems": True,
        "skusFilter": "ALL_AVAILABLE",
        "simulationBehavior": "default",
        "installmentCriteria": "MAX_WITHOUT_INTEREST",
        "productOriginVtex": False,
        "map": "ft",
        "query": "medicamentos",
        "orderBy": "OrderByScoreDESC",
        "from": from_index,
        "to": to_index,
        "selectedFacets": [
            {
                "key": "ft",
                "value": "medicamentos"
            }
        ],
        "fullText": "medicamentos",
        "operator": "and",
        "fuzzy": "0",
        "searchState": None,
        "facetsBehavior": "Static",
        "categoryTreeBehavior": "default",
        "withFacets": False,
        "advertisementOptions": {
            "showSponsored": True,
            "sponsoredCount": 3,
            "advertisementPlacement": "top_search",
            "repeatSponsoredProducts": True
        }
    }
    
    payload = {
        "operationName": "productSearchV3",
        "variables": variables,
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "9177ba6f883473505dc99fcf2b679a6e270af6320a157f0798b92efeab98d5d3",
                "sender": "vtex.store-resources@0.x",
                "provider": "vtex.search-graphql@0.x"
            }
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Enviando a requisição
    response = requests.post(url, json=payload, headers=headers)
    
    produtos_encontrados = []
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            
            # Extrair os produtos da resposta
            data = response_data.get('data', {}).get('productSearch', {}).get('products', [])
            
            for produto in data:
                # Extrair nome e preço
                nome = produto.get('productName', 'Nome não encontrado')
                preco = produto.get('priceRange', {}).get('sellingPrice', {}).get('highPrice', 'Preço não encontrado')
                ean = produto.get('items', [{}])[0].get('ean', 'EAN não encontrado')
                
                # Adicionar produto à lista de resultados
                produtos_encontrados.append({
                    'nome': nome,
                    'preco': preco,
                    'ean': ean
                })
                
                # Imprimir informações (opcional)
                print(f"Nome: {nome}")
                print(f"Preço: {preco}")
                print(f"EAN: {ean}")
                print('-' * 40)
                
        except ValueError as e:
            print(f"Erro ao analisar o JSON: {e}")
    else:
        print(f"Erro: {response.status_code}")
    
    return produtos_encontrados

# Exemplo de uso
if __name__ == "__main__":
    total_paginas = 45  # Número total de páginas
    produtos_por_pagina = 18  # Número de produtos por página, ajuste conforme necessário

    for pagina in range(1, total_paginas + 1):
        print(f"\n=== PÁGINA {pagina} ===")
        produtos_pagina = buscar_produtos_paginados(pagina=pagina, produtos_por_pagina=produtos_por_pagina)
        for produto in produtos_pagina:
            print(f"Nome: {produto['nome']}, Preço: {produto['preco']}, EAN: {produto['ean']}")