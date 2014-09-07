import configparser
import logging

def config():
    config = configparser.ConfigParser()
    config.read('ingrex.ini')
    logging.basicConfig(filename ='ingrex.log', filemode='w',
        format='%(asctime)s - %(levelname)s: %(message)s',
        level = logging.WARNING)
    return config

