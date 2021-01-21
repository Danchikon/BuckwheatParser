from time import sleep
from parsers.rozetka import *
from colorama import Fore


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

        self.updateDB(documents)

    def updateDB(self, docs):
        try:
            self.dataBase.drop_collection('buckwheat_groats')
            self.dataBase.buckwheat_groats.insert_many(docs)
        except Exception as e:
            print(Fore.RED, 'error', 'can not update db', e, Fore.RESET, sep=' | ')
        else:
            print(Fore.GREEN, '- db successfully updated -', Fore.RESET)

    # def updateChartsInfo(self):
    #     while self.status:
    #         sleep(DELAY)

    def start(self):
        self.runParsing()

    def runParsing(self):
        while self.status:

            self.parseBuckwheat()

            sleep(DELAY)
