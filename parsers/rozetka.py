from bs4 import BeautifulSoup
from scripts import *
from _settings import *
from colorama import Fore


class RozetkaParser:
    def parse(self):
        buckwheats = []

        pages = self.getPagesCount()
        print(' - count of pages:', pages)

        for page in range(1, pages + 1):
            print(' - page:', page)
            page = getPage(ROZETKA_URL + f'page={page};vid-225787=grechka/')

            try:
                soup = BeautifulSoup(page.text, MARKUP)

                products = soup.find_all('li', class_='catalog-grid__cell')
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
                picture = product.find('a', class_='goods-tile__picture')
                productImage = picture.find(class_='lazy_img_hover')['src']

                heading = product.find('a', class_='goods-tile__heading')
                productHref = heading['href']
                productName = heading['title']

                productPrice = float(product.find('span', class_='goods-tile__price-value').text)

                productPage = getPage(productHref + 'characteristics/')
                soup = BeautifulSoup(productPage.text, MARKUP)

                characteristics = soup.find_all('div', class_='characteristics-full__item')

                characteristicsDict = self.parseCharacteristics(characteristics)
                productWeight, productCountry = self.getCharacteristics(characteristicsDict)

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
                    'country': productCountry,
                    'site': 'Rozetka',
                    'image': productImage,
                    'link': productHref
                }

                buckwheats.append(buckwheat)
            except Exception as e:
                print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')

        return buckwheats

    def getCharacteristics(self, characteristics):
        # ===================================
        productWeight = None
        try:
            productWeight = characteristics['Вага']
            index = productWeight.find(' ')

            if productWeight[index + 1:] == 'кг':
                productWeight = float(productWeight[:index]) * 1000
            else:
                productWeight = float(productWeight[:index])
        except Exception as e:
            print(Fore.RED, 'error', 'can not get a weight', e, Fore.RESET, sep=' | ')
        # ===================================
        productCountry = None
        try:
            productCountry = characteristics['Країна-виробник']
        except Exception as e:
            print(Fore.RED, 'error', 'can not get a country', e, Fore.RESET, sep=' | ')
        # ===================================

        try:
            productCount = int(characteristics['Кількість в упаковці, шт.'])
        except Exception as e:
            print(Fore.RED, 'error', 'can not get a count', e, Fore.RESET, sep=' | ')
        else:
            productWeight *= productCount

        return productWeight, productCountry

    def parseCharacteristics(self, characteristics):
        characteristicsDict = {}

        for characteristic in characteristics:
            try:
                key = characteristic.find(class_='characteristics-full__label').text
                value = characteristic.find(class_='characteristics-full__value').text
            except Exception as e:
                print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
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
            print(Fore.RED, 'error', e, Fore.RESET, sep=' | ')
            return 1
        else:
            return count

    def __str__(self):
        return 'RozetkaParser'
