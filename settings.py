import os.path
from jinja2 import Environment, FileSystemLoader
import shelve

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_FILES = os.path.join(PROJECT_ROOT, 'templates')
STATIC_FILES = os.path.join(PROJECT_ROOT, 'static')
XML_FILES = os.path.join(PROJECT_ROOT, 'XML')

SHELVE_FILE_NAME = os.path.join(PROJECT_ROOT, 'maps.shelve')


conf = {
    'global': {'server.socket_host': '127.0.0.1',
               'server.socket_port': 8282,
               'server.thread_pool': 10,
               },
    '/static':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': STATIC_FILES,
         },
    }

db = shelve.open(SHELVE_FILE_NAME)
templates = Environment(loader=FileSystemLoader(TEMPLATE_FILES))
