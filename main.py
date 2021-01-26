from _parser import BuckwheatParser
from _settings import *
from parsers.rozetka import RozetkaParser
from parsers.metro import MetroParser
from parsers.prom import PromParser
import colorama
from colorama import Fore
import pymongo
import socket

print(socket.gethostbyname(socket.gethostname()))


def main():
    try:
        colorama.init()
        client = pymongo.MongoClient(MONGO_CONNECTION, connectTimeoutMS=1000000, socketTimeoutMS=1000000)
    except Exception as e:
        print(Fore.RED, 'error', 'can not connect to the mongo client', e, Fore.RESET, sep=' | ')
    else:
        print(Fore.GREEN, '- connected successfully -', Fore.RESET)
        parsers = [MetroParser(), RozetkaParser(), PromParser()]  # [RozetkaParser(), MetroParser(), PromParser()]

        buckwheatParser = BuckwheatParser(parsers, client.buckwheat)
        buckwheatParser.start()


if __name__ == '__main__':
    main()

