from bs4 import BeautifulSoup
from scripts import *
from _settings import *


class RozetkaParser:
    def parse(self):
        buckwheats = []

        pages = self.getPagesCount()
        print('count of pages:', pages)

        for page in range(1, pages + 1):
            print('page:', page)
            page = getPage(ROZETKA_URL + f'page={page};vid-225787=grechka/')

            try:
                soup = BeautifulSoup(page.text, MARKUP)

                products = soup.find_all('li', class_='catalog-grid__cell')
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
                productID = product.find('div', class_='goods-tile__inner')['data-goods-id']

                title = product.find('a', class_='goods-tile__heading')
                productHref = title['href']
                productName = title['title']

                try:
                    productPrice = float(product.find('span', class_='goods-tile__price-value').text)
                except Exception as e:
                    print('error', 'can not get a price', e, sep=' | ')
                    productPrice = None

                productPage = getPage(productHref + 'characteristics/')
                soup = BeautifulSoup(productPage.text, MARKUP)

                characteristics = soup\
                    .find(class_='characteristics-full__list')\
                    .find_all('div', class_='characteristics-full__item')
                characteristicsDict = self.parseCharacteristics(characteristics)

                # ===================================
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
                # ===================================
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
                # ===================================

                buckwheat = {
                    '_id': productID,
                    'name': productName,
                    'price': productPrice,
                    'price_g': price_g,
                    'weight': productWeight,
                    'country': productCountry,
                    'site': 'Rozetka',
                    'link': productHref
                }

                buckwheats.append(buckwheat)
            except Exception as e:
                print('error', e, sep=' | ')

        return buckwheats

    def parseCharacteristics(self, characteristics):
        characteristicsDict = {}

        for characteristic in characteristics:
            try:
                key = characteristic.find(class_='characteristics-full__label').text
                value = characteristic.find(class_='characteristics-full__value').text
            except Exception as e:
                print('error', e, sep=' | ')
            else:
                characteristicsDict.update([(key, value)])

        return characteristicsDict

    def getPagesCount(self):
        page = getPage(ROZETKA_URL + 'vid-225787=grechka/')

        try:
            soup = BeautifulSoup(page.text, MARKUP)
            pages = soup.find_all('li', class_='pagination__item')
            count = int(pages[len(pages) - 1].text)
        except Exception as e:
            print('error', e, sep=' | ')
            return 1
        else:
            return count