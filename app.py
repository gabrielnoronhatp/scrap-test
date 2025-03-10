import requests
from bs4 import BeautifulSoup

# URL da página (substitua pela URL correta)
url = 'https://www.bemolfarma.com.br/'

# Fazendo a requisição HTTP
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parseando o conteúdo HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando todos os contêineres de produtos
    product_containers = soup.find_all('section', class_='vtex-product-summary-2-x-container')

    # Iterando sobre os contêineres de produtos
    for container in product_containers:
        # Extraindo o nome do produto
        name_container = container.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
        if name_container:
            name_element = name_container.find('span', class_='vtex-product-summary-2-x-productBrand')
            name = name_element.text.strip() if name_element else 'Nome não encontrado'
        else:
            name = 'Nome não encontrado'

        # Extraindo o preço do produto
        price_element = container.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
        price = price_element.text.strip() if price_element else 'Preço não encontrado'

        # Exibindo os dados
        print(f"Nome: {name}")
        print(f"Preço: {price}")
        print("-" * 40)
else:
    print(f"Erro ao acessar a página: {response.status_code}")