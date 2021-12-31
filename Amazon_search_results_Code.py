# For webscraping
from bs4 import BeautifulSoup
# Chrome driver
from selenium import webdriver
# Chrome driver manager
from webdriver_manager.chrome import ChromeDriverManager
# For current data and time
from datetime import datetime
# For writing results to CSV file
import csv

# Function for generating CSV file with product information
def generate_csv(search_input, product_info):
    search_input_mod = search_input.replace(' ', '_')
    current_datetime = datetime.now().strftime("%y%m%d%H%M%S")
    filename = search_input_mod + '_' + current_datetime + '.csv'
    
    with open(filename, 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Price', 'Rating (Out of 5)', 'No. of Reviews', 'Product Link'])
        writer.writerows(product_info)
        print("Product info has been written to " + filename)

# Function for generating URL based on user search input
def get_url(search_input):
    search_input_mod = search_input.replace(' ', '+')
    url = 'https://www.amazon.in/s?k=' + search_input_mod
    return url

# Function for extracting product data with exception handling
def extract_data(product):
    
    try:
        name = product.h2.a.text.strip()
        price = product.find('span', 'a-price').find('span', 'a-offscreen').text
        link = 'https://www.amazon.in' + product.h2.a.get('href')
    except:
        return
    
    try: 
        ratings = product.find('span', 'a-icon-alt').text.strip(' out of 5 stars')
        num_of_reviews = product.find('span', 'a-size-base').text
    except:
        ratings = ''
        num_of_reviews = ''
    
    info = (name, price, ratings, num_of_reviews, link)
    return info

def main():
    # Run main program
    # Initialize webdriver for chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())

    print('________________________')
    print('AMAZON.IN SEARCH RESULTS')
    print('************************')
    print('This program exports the')
    print('results of user search')
    print('query into a CSV file')

    continue_search = True

    while continue_search:
        product_info = []

        search_input = input('\nSearch for: ')
        url = get_url(search_input)

        # To get product data in each page of 20 pages long search result
        for page_num in range(1, 21):
            url_full = url + '&page=' + str(page_num)
            driver.get(url_full)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
    
            product_data = soup.find_all('div', {'data-component-type': 's-search-result'})
            for product in product_data:
                info = extract_data(product)
                if info:
                    product_info.append(info)

        generate_csv(search_input, product_info)

        while True:
            continue_response = input('\nWould you like to search again? (Y/N): ')
            if continue_response.lower() == 'y':
                continue_search = True
                break
            elif continue_response.lower() == 'n':
                continue_search = False
                break
            else:
                print("Enter a valid response.")
                continue

if __name__ == "__main__":
    main()