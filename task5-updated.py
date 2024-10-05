import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_amazon_products(url):
    # Send a GET request to the website with additional headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    
    # Retry logic for handling server issues
    for attempt in range(5):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        print(f"Failed to retrieve the page. Status code: {response.status_code}. Retrying in 5 seconds...")
        time.sleep(5)
    else:
        print("Failed to retrieve the page after multiple attempts.")
        return []

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # List to store product information
    products = []

    # Find product containers
    for product in soup.find_all('div', class_='s-main-slot s-result-list s-search-results sg-row'):
        for item in product.find_all('div', class_='s-result-item'):
            # Extract product name
            name = item.h2.text if item.h2 else 'N/A'
            
            # Extract price
            price = item.find('span', class_='a-price')
            if price:
                price = price.find('span', class_='a-offscreen').text
            else:
                price = 'N/A'
            
            # Extract rating
            rating = item.find('span', class_='a-icon-alt')
            if rating:
                rating = rating.text
            else:
                rating = 'N/A'
            
            # Add product details to the list
            products.append({'Name': name, 'Price': price, 'Rating': rating})

    return products

def save_to_csv(products, filename):
    # Specify the CSV file to write the data
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Price', 'Rating'])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

# URL of the Amazon search results page (you can change this to any valid page)
url = 'https://www.amazon.com/s?k=laptops'
products = scrape_amazon_products(url)

if products:
    # Save the extracted products to a CSV file
    save_to_csv(products, 'products.csv')
    print(f"Extracted {len(products)} products and saved to products.csv")
else:
    print("No products found.")