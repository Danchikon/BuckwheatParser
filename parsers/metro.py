from bs4 import BeautifulSoup
from scripts import *
from _settings import *
from colorama import Fore


class MetroParser:
    def parse(self):
        buckwheats = []

        # pages = self.getPagesCount()
        pages = 1
        print(' - count of pages:', pages)
        for page in range(1, pages + 1):
                print(' - page:', page)
                page = getPage(METRO_URL + f'?page={page}')

                try:
                    soup = BeautifulSoup(page.text, MARKUP)
                    
                    products = soup.find_all('div', class_='products-box__list-item')
                except Exception as e:
                    print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
                else:
                    extraBuckwheats = self.parseProducts(products)
                    buckwheats += extraBuckwheats

        return buckwheats

    def parseProducts(self, products):
        buckwheats = []

        for product in products:
            try:
                picture = product.find('div', class_='product-tile__image')
                productImage = picture.find(class_='product-tile__image-i')['src']

                title = product.find('a', class_='product-tile')
                productHref = title['href']
                productName = title['title']

                productPrice = float(product.find('span', class_='Price__value_caption').text)

                try:
                    productWeight = product.find('div', class_='product-tile__weight').text
                    index = productWeight.find(' ')
                    if productWeight[index + 1:] == 'кг':
                        productWeight = float(productWeight[:index]) * 1000
                    else:
                        productWeight = float(productWeight[:index])
                except Exception as e:
                    print(Fore.RED, 'error', 'can not get a weight', e, Fore.RESET, sep=' | ')
                    productWeight = None

                try:
                    price_g = productPrice / productWeight
                except Exception as e:
                    print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
                    price_g = None

                buckwheat = {
                    'name': productName,
                    'price': productPrice,
                    'price_g': price_g,
                    'weight': productWeight,
                    'country': None,
                    'site': 'Metro',
                    'image': productImage,
                    'link': 'https://metro.zakaz.ua' + productHref
                }

                buckwheats.append(buckwheat)
            except Exception as e:
                print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')

        return buckwheats

    def __str__(self):
        return 'MetroParser'
    
    # def getPagesCount(self):
    #     page = getPage(METRO_URL)
    #     try:
    #         soup = BeautifulSoup(page.text, MARKUP)
    #         pages = soup.find_all('a', class_='pagination__item')
    #         count = int(pages[len(pages) - 1].text)
    #     except Exception as e:
    #         print('error', e, sep=' | ')
    #         return 1
    #     else:
    #         return count


