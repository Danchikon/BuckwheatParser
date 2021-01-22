from bs4 import BeautifulSoup
from scripts import *
from _settings import *


class PromParser:
    def parse(self):
        buckwheats = []

        pages = self.getPagesCount()
        print('count of pages:', pages)
        for page in range(1, pages + 1):
                print('page:', page)
                page = getPage(PROM_URL + f'&page={page}')
                

                try:
                    soup = BeautifulSoup(page.text, MARKUP)
                    
                    products = soup.find_all('div', attrs={"data-qaid": "product_block"})
                except Exception as e:
                    print('error', e, sep=' | ')
                else:
                    extraBuckwheats = self.parseProducts(products)
                    buckwheats += extraBuckwheats

        return buckwheats
    def parseProducts(self, products):
        buckwheats = []

        for product in products:
            try:
                title = product.find('a', attrs={"data-qaid": "product_link"})
                productHref = "https://prom.ua"+title['href']
                productName = title['title']
                try:
                    productPrice = float(product.find('span',attrs={"data-qaid": "product_price"}).text)

                except Exception as e:
                    print('error', 'can not get a price', e, sep=' | ')
                    productPrice = None
                
                productPage = getPage(productHref)
                soup = BeautifulSoup(productPage.text, MARKUP)

                characteristics = soup\
                    .find(attrs={"data-qaid":'attributes'})\
                    .find_all('li', class_='ek-list__item')
                characteristicsDict = self.parseCharacteristics(characteristics)

                productWeight = None
                try:
                    productWeight = characteristicsDict['Вага']
                    index = productWeight.find(' ')
                    if productWeight[index + 1:] == 'кг':
                        productWeight = float(productWeight[:index]) * 1000
                    else:
                        productWeight = float(productWeight[:index])
                except Exception as e:
                    print('error', 'can not get a weight', e, sep=' | ')


                productCountry = None
                try:
                    productCountry = characteristicsDict['Країна походження']
                except Exception as e:
                    print('error', 'can not get a country', e, sep=' | ')

                try:
                    price_g = productPrice / productWeight
                except Exception as e:
                    print('error', e, sep=' | ')
                    price_g = None

                buckwheat = {
                    
                    'name': productName,
                    'price': productPrice,
                    'price_g': price_g,
                    'weight': productWeight,
                    'country': productCountry,
                    'site': 'Metro',
                    'link': "https://prom.ua"+productHref
                }

                buckwheats.append(buckwheat)
            except Exception as e:
                print('error', e, sep=' | ')

        return buckwheats

    def parseCharacteristics(self, characteristics):
        characteristicsDict = {}
        for characteristic in characteristics:
            try:
                key = characteristic.find(class_='big-product-card__entry-title').text
                value = characteristic.find(class_='big-product-card__entry-value').text
            except Exception as e:
                print('error', e, sep=' | ')
            else:
                characteristicsDict.update([(key, value)])

        return characteristicsDict
    
    def getPagesCount(self):
        page = getPage(PROM_URL)
        try:
            soup = BeautifulSoup(page.text, MARKUP)
            pages = soup.find_all('button', class_='ek-button')
            count = int(pages[len(pages) - 1].text)
        except Exception as e:
            print('error', e, sep=' | ')
            return 1
        else:
            return count
