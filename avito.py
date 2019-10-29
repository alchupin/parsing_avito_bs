import csv

import requests
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(
            (data['title'],
            data['price'],
            data['metro'],
            data['url'])
        )

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
        try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        except:
            title = ''
        if not 'asus' in title.lower():
            continue
        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''
        try:
            metro = ad.find('div', class_='item-address').find('span', class_='item-address-georeferences-item__content').text
        except:
            metro = ''
        print(title, url, price, metro)
        data = {
            'title': title,
            'url': url,
            'price': price,
            'metro': metro
        }

        write_csv(data)

def main():
    html = 'https://www.avito.ru/moskva/noutbuki?cd=1&q=asus'
    base_url = 'https://www.avito.ru/moskva/noutbuki?'
    page_part = 'p='
    query_part = '&q=asus'

    total_pages = get_total_pages(get_html(html))
    print(total_pages)

    # for i in range(1, (total_pages+1)):
    #     gen_url = base_url + page_part + str(i) + query_part
    #     html = get_html(gen_url)

    for i in range(1, 3):
        gen_url = base_url + page_part + str(i) + query_part
        html = get_html(gen_url)

    get_page_data(html)





if __name__ == '__main__':
    main()