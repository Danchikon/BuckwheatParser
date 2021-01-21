from _parser import BuckwheatParser
from _settings import *
from parsers.rozetka import RozetkaParser
from parsers.metro import MetroParser
import colorama
from colorama import Fore
import pymongo


def main():
    try:
        colorama.init()
        client = pymongo.MongoClient(MONGO_CONNECTION)
    except Exception as e:
        print(Fore.RED, 'error', 'can not connect to the mongo client', e, Fore.RESET, sep=' | ')
    else:
        print(Fore.GREEN, '- connected successfully -', Fore.RESET)
        parsers = [RozetkaParser(), MetroParser(),  ]  # [RozetkaParser(), MetroParser(), PromParser()]

        buckwheatParser = BuckwheatParser(parsers, client.buckwheat)
        buckwheatParser.start()


if __name__ == '__main__':
    main()

