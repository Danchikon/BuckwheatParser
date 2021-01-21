from time import sleep
from parsers.rozetka import *


class BuckwheatParser:
    def __init__(self, parsers, db):
        self.dataBase = db
        self.status = True
        self.parsers = parsers

    def parseBuckwheat(self):
        documents = []
        # scrapMetro()
        for parser in self.parsers:
            buckwheat = parser.parse()
            documents.append(buckwheat)

        self.updateDB(documents)

    def updateDB(self, doc):
        try:
            self.dataBase.drop_collection('buckwheat_groats')
            self.dataBase.buckwheat_groats.insert_many(doc)
        except Exception as e:
            print('error', 'can not update db', e, sep=' | ')

    # def updateChartsInfo(self):
    #     while self.status:
    #         sleep(DELAY)

    def start(self):
        self.runScrap()

    def runScrap(self):
        while self.status:

            self.parseBuckwheat()

            sleep(DELAY)
