#coding=utf-8

from __future__ import unicode_literals
from io import open

import logging
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

Config = configparser.ConfigParser()
with open('ingrex.ini', encoding='utf-8') as file:
    Config.readfp(file)

logging.basicConfig(filename ='ingrex.log', filemode='w',
    format='%(asctime)s - %(levelname)s: %(message)s',
    level = logging.WARNING)

