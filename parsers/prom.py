from bs4 import BeautifulSoup
from colorama import Fore

from scripts import *
from _settings import *


class PromParser:
    def parse(self):
        buckwheats = []

        pages = self.getPagesCount()
        print('count of pages:', pages)
        for page in range(1, pages + 1):
                print('page:', page)
                page = getPage(PROM_URL + f';{page}')

                try:
                    soup = BeautifulSoup(page.text, MARKUP)

                    productList = soup.find('div', attrs={"data-qaid": "product_gallery"})
                    products = productList.find_all('div', class_='ek-grid__item')
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
                title = product.find('a', attrs={"data-qaid": "product_link"})
                productHref = "https://prom.ua" + title['href']
                productName = title['title']

                productPage = getPage(productHref)
                soup = BeautifulSoup(productPage.text, MARKUP)

                try:
                    priceQaid = soup.find('span', attrs={"data-qaid": "product_price"})
                    productPrice = float(priceQaid['data-qaprice'])

                except Exception as e:
                    print(Fore.RED, 'error', 'can not get a price', e, Fore.RESET, sep=' | ')
                    productPrice = None

                imageQaid = soup.find('span', attrs={"data-qaid": "image_block"})
                productImage = imageQaid.find('img')['src']

                characteristics = soup.find('li', attrs={"data-qaid": "attributes"}).find_all(class_='ek-grid')
                characteristicsDict = self.parseCharacteristics(characteristics)

                productWeight = None
                try:
                    productWeight = characteristicsDict['Вага']
                    index = productWeight.find(' ')
                    if productWeight[index + 1:] == 'кг':
                        productWeight = float(productWeight[:index]) * 1000
                    elif productWeight[index + 1:] == 'г':
                        productWeight = float(productWeight[:index])
                    else:
                        productWeight = None
                except Exception as e:
                    print(Fore.RED, 'error', 'can not get a weight', e, Fore.RESET, sep=' | ')
                #
                #
                productCountry = None
                try:
                    productCountry = characteristicsDict['Країна виробник']
                except Exception as e:
                    print(Fore.RED, 'error', 'can not get a country', e, Fore.RESET, sep=' | ')

                # try:
                #     price_g = productPrice / productWeight
                # except Exception as e:
                #     print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
                #     price_g = None

                buckwheat = {
                    
                    'name': productName,
                    'price': productPrice,
                    'price_g': None,
                    'weight': productWeight,
                    'country': productCountry,
                    'site': 'Prom',
                    'image': productImage,
                    'link': productHref
                }

                buckwheats.append(buckwheat)
            except Exception as e:
                print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')

        return buckwheats

    def parseCharacteristics(self, characteristics):
        characteristicsDict = {}
        for characteristic in characteristics:
            try:
                data = characteristic.find_all(class_='ek-grid__item')
                key = data[0].text
                value = data[1].text
            except Exception as e:
                print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
            else:
                characteristicsDict.update([(key, value)])

        return characteristicsDict
    
    def getPagesCount(self):
        page = getPage(PROM_URL)
        try:
            soup = BeautifulSoup(page.text, MARKUP)
            pages = soup.find_all('button', class_='ek-button')
            count = int(pages[len(pages) - 2].text)
        except Exception as e:
            print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
            return 1
        else:
            return count

    def __str__(self):
        return 'PromParser'