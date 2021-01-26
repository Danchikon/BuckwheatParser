from time import sleep, struct_time, time, localtime
from parsers.rozetka import *
from colorama import Fore
from pymongo.client_session import ClientSession


class BuckwheatParser:
    def __init__(self, parsers, db):
        self.dataBase = db
        self.status = True
        self.parsers = parsers

    def parseBuckwheat(self):
        documents = []
        # scrapMetro()
        for parser in self.parsers:
            print(Fore.BLUE, f'<- {parser} started ->', Fore.RESET)
            buckwheat = parser.parse()
            documents += buckwheat

        self.updateDB(self.sortDoc(documents))

    def sortDoc(self, docs):
        res = docs
        for i in range(len(res)):
            for j in range(len(res)):
                try:
                    if res[i]['price'] < res[j]['price']:
                        temp = res[i]
                        res[i] = res[j]
                        res[j] = temp
                except:
                    temp = res[i]
                    res[i] = res[j]
                    res[j] = temp
        return res

    def updateDB(self, docs):
        try:
            self.dataBase.drop_collection('buckwheat_groats')
            sleep(1)
            self.dataBase.buckwheat_groats.insert_many(docs)
            self.dataBase.buckwheat_groats.create_index([('name', 'text')])
        except Exception as e:
            print(Fore.RED, 'error', 'can not update db', e, Fore.RESET, sep=' | ')
        else:
            print(Fore.GREEN, '- db successfully updated -', Fore.RESET)

        try:
            self.updateChartsInfo(docs)
        except Exception as e:
            print(Fore.RED, 'error', 'can not update charts', e, Fore.RESET, sep=' | ')
        else:
            print(Fore.GREEN, '- charts successfully updated -', Fore.RESET)

    def updateChartsInfo(self, docs):
        count = 0
        price = 0

        for doc in docs:
            try:
                price += doc['price_g']
                count += 1
            except TypeError:
                pass

        try:
            avr_price = price / count
        except ZeroDivisionError:
            pass
        else:
            tm = localtime(time())
            self.dataBase.charts_info.insert({
                'avr_price': avr_price,
                'year': tm.tm_year,
                'month': tm.tm_mon,
                'day': tm.tm_mday,
            })

    def start(self):
        self.runParsing()

    def runParsing(self):
        while self.status:

            self.parseBuckwheat()

            sleep(DELAY)
