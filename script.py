import requests
from bs4 import BeautifulSoup
from queries import INSERT_QUERY, CREATE_TABLE_QUERY
from dbConnection import get_db_connection

def extract_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.select('#maincontent .products .product-item-info')
    return products

def transform_product_data(product):
    try:
        name = product.select_one('.product-item-name a').text.strip()
        sku = product.select_one('.skuDesktop').text.strip()
        description = product.select_one('.product-item-description p').text.strip()
        
        price = float(product.select_one('.price').text.strip().replace('DT', '').replace(',', '.').replace('\xa0', '').strip())
        
        availability = product.select_one('.stock')
        if availability and 'Epuisé' in availability.text:
            availability_status = 'Out of Stock'
        else:
            availability_status = 'In Stock'
        
        return {
            'name': name,
            'sku': sku,
            'description': description,
            'price': price,
            'availability': availability_status
        }
    except AttributeError:
        return None

def load_product_data_to_db(products_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    
    for product in products_data:
        if product:
            cursor.execute(INSERT_QUERY, (
                product['price'],
                product['sku'],
                product['name'],
                product['description'],
                product['availability']
            ))
    conn.commit()
    cursor.close()
    conn.close()

def run_etl_process(url):
    print("Extracting product data...")
    products = extract_product_data(url)
    
    print("Transforming product data...")
    transformed_data = [transform_product_data(product) for product in products]
    
    print("Loading product data to the database...")
    load_product_data_to_db(transformed_data)
    
    print("ETL process completed successfully!")

if __name__ == "__main__":
    url = 'https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable.html'
    run_etl_process(url)
