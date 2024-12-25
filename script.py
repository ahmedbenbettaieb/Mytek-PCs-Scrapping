import requests
from bs4 import BeautifulSoup
from queries import INSERT_QUERY, CREATE_TABLE_QUERY
from dbConnection import get_db_connection

def insert_product_data(price, ref, name, description, availability):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(INSERT_QUERY, (price, ref, name, description, availability))
    conn.commit()
    cursor.close()
    conn.close()

url = 'https://www.mytek.tn/informatique/ordinateurs-portables/pc-portable.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
products = soup.select('#maincontent .products .product-item-info')

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(CREATE_TABLE_QUERY)
conn.commit()

for product in products:
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

        insert_product_data(price, sku, name, description, availability_status)
    
    except AttributeError:
        continue

cursor.close()
conn.close()

print("Product data has been inserted into the database.")
