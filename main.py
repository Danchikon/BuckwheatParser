from _parser import Parser
from _settings import *
from parsers.rozetka import RozetkaParser
import pymongo


def main():
    try:
        client = pymongo.MongoClient(MONGO_CONNECTION)
    except Exception as e:
        print('error', 'can not connect to the mongo client', e, sep=' | ')
    else:
        parsers = [RozetkaParser, ]  # [RozetkaParser, MetroParser, PromParser]

        buckwheatParser = Parser(parsers, client.buckwheat)
        buckwheatParser.start()


if __name__ == '__main__':
    main()

