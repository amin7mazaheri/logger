import logging
import json
import os

MODE_TYPES = ['DEBUG', 'PRODUCTION']
LEVEL_NAMES = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'critical': logging.CRITICAL,
    'error': logging.ERROR
    }

LEVEL_INTS = {
    10: logging.DEBUG,
    20: logging.INFO,
    30: logging.WARNING,
    40: logging.ERROR,
    50: logging.CRITICAL
    }

EXTRA = {'module_name': None}

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(path, 'r') as confs:
    try:
        custom_configs = json.load(confs)
    except:
        custom_configs = dict()

PATH = custom_configs.get('PATH', '/tmp/logs.log')
LEVEL = custom_configs.get('LEVEL', logging.WARN)
MODE = custom_configs.get('MODE', 'DEBUG')
FORMAT = custom_configs.get('FORMAT', logging.Formatter('%(asctime)s %(levelname)s [Module: %(module_name)s]: %(message)s'))