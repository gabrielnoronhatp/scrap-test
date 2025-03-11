import requests
import base64
import json

def buscar_produtos(collection_id=None, category=None, specification_filters=None, from_index=0, to_index=15):
  
    # URL do endpoint GraphQL
    url = "https://www.bemolfarma.com.br/_v/segment/graphql/v1"
    
    # Preparar as variáveis para a consulta
    variables = {
        "hideUnavailableItems": True,
        "skusFilter": "ALL_AVAILABLE",
        "installmentCriteria": "MAX_WITHOUT_INTEREST",
        "category": category or "",
        "collection": collection_id or "",
        "specificationFilters": specification_filters or [],
        "orderBy": "",
        "from": from_index,
        "to": to_index,
        "shippingOptions": [],
        "variant": "",
        "advertisementOptions": {
            "showSponsored": False,
            "sponsoredCount": 2,
            "repeatSponsoredProducts": False,
            "advertisementPlacement": "home_shelf"
        }
    }
    
 
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
            
            data = response_data.get('data', {}).get('products', {})
            
            if isinstance(data, list):
                produtos = data
            else:
                produtos = data.get('edges', [])
                
            for produto in produtos:
                # Extrair o nó do produto se estiver em formato de edges
                if 'node' in produto:
                    produto_info = produto.get('node', {})
                else:
                    produto_info = produto
                
                nome = produto_info.get('productName', produto_info.get('name', 'Nome não encontrado'))
                
                preco = None
                if 'price' in produto_info and 'sellingPrice' in produto_info.get('price', {}):
                    preco = produto_info.get('price', {}).get('sellingPrice')
                elif 'priceRange' in produto_info and 'sellingPrice' in produto_info.get('priceRange', {}):
                    preco = produto_info.get('priceRange', {}).get('sellingPrice', {}).get('lowPrice')
                
                ean = 'EAN não encontrado'
                items = produto_info.get('items', [])
                if items and len(items) > 0:
                    ean = items[0].get('ean', 'EAN não encontrado')
                
                produtos_encontrados.append({
                    'nome': nome,
                    'preco': preco,
                    'ean': ean,
                    'produto_completo': produto_info  
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

# Exemplo de uso para diferentes páginas/categorias
if __name__ == "__main__":
    # Exemplo 1: Buscar produtos da coleção "Destaques da Semana" (ID 138)
    print("=== DESTAQUES DA SEMANA ===")
    destaques = buscar_produtos(collection_id="138", 
                               specification_filters=["specificationFilter_Tarja do Medicamento:Venda Livre"])
    
    # Exemplo 2: Buscar produtos de uma categoria específica
    print("\n=== CATEGORIA VITAMINAS ===")
    vitaminas = buscar_produtos(category="131")  # Substitua pelo ID correto da categoria
    
    # Exemplo 3: Buscar produtos com filtros específicos
    print("\n=== MEDICAMENTOS GENÉRICOS ===")
    genericos = buscar_produtos(specification_filters=["specificationFilter_Tipo de Medicamento:Genérico"])
    
    
    