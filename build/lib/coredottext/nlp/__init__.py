import os
# from .parse import generate_graph, draw_label_graph, get_result
from .pos import TextClient
from .tfidf import Tfidf

__version__ = '0.0.1'
__license__ = 'UNIST'
__author__ = 'Core.Today'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'pos'
]
