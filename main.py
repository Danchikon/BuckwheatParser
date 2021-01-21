from _parser import BuckwheatParser
from _settings import *
from parsers.rozetka import RozetkaParser
from parsers.metro import MetroParser
import pymongo


def main():
    try:
        client = pymongo.MongoClient(MONGO_CONNECTION)
    except Exception as e:
        print('error', 'can not connect to the mongo client', e, sep=' | ')
    else:
        parsers = [RozetkaParser(), MetroParser(),  ]  # [RozetkaParser(), MetroParser(), PromParser()]

        buckwheatParser = BuckwheatParser(parsers, client.buckwheat)
        buckwheatParser.start()


if __name__ == '__main__':
    main()

