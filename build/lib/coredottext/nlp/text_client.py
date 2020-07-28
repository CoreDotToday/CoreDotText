# -*- coding: utf-8 -*-
import requests
import json
import uuid
import logging
import re
from coredottext.nlp import database

__author__ = "Core.Today"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)

# Not work...

class TextClient:
    HOST = "localhost"
    PORT = "7123"

    bucket = ""  # Text Bucket
    tag = dict()

    custom = list()  # custom_keywords
    custom_pos = list()  # custom_keywords_pos

    documents = dict()
    dictionary = None
    corpus = None
    corpus_key = None

    database_type = 0  # 0: memory, 1: MongoDB

    def __init__(
            self,
            api_host=None,
            api_port=None,
            api_key=None,
            db_host=None,
            db_port=None,
            bucket="",
            **kwargs):
        """Client for NLP.

        The client object is .

            try:
                # Python 3.x
                from coredottext import nlp
            except: ImportError:
                from

        .. note:: TextClient creation will block waiting for answers from DNS

        .. warning:: It use a api.core.today API URI

        :Parameters:
          - `host` (require):

          | **Authentication:**
          - `username`: A string.
          - `password`: A string.

        Examples
        --------
        >>> import coredottext.nlp as nlp
        >>>
        >>> text = nlp.TextClient(api_host='unist.core.today')
        >>> text.bucket = "안녕하세요 파이썬을 재밌게 배우고 있습니다 하하하"
        >>> text.tagging()
        {0: {'term': '안녕',
          'pos': 'NNG',
          'feature': ['행위', 'T', '안녕', '*', '*', '*', '*']},
         1: {'term': '하',
          'pos': 'XSV',
          'feature': ['*', 'F', '하', '*', '*', '*', '*']},
         10: {'term': '습니다',
          'pos': 'EF',
          'feature': ['*', 'F', '습니다', '*', '*', '*', '*']},
         11: {'term': '하하하',
          'pos': 'IC',
          'feature': ['*', 'F', '하하하', '*', '*', '*', '*']},
         2: {'term': '세요',
          'pos': 'EP+EF',
          'feature': ['*', 'F', '세요', 'Inflect', 'EP', 'EF', '시/EP/*+어요/EF/*']},
         3: {'term': '파이썬',
          'pos': 'NNP',
          'feature': ['*', 'T', '파이썬', '*', '*', '*', '*']},
         4: {'term': '을',
          'pos': 'JKO',
          'feature': ['*', 'T', '을', '*', '*', '*', '*']},
         5: {'term': '재밌',
          'pos': 'VA',
          'feature': ['*', 'T', '재밌', '*', '*', '*', '*']},
         6: {'term': '게', 'pos': 'EC', 'feature': ['*', 'F', '게', '*', '*', '*', '*']},
         7: {'term': '배우',
          'pos': 'VV',
          'feature': ['*', 'F', '배우', '*', '*', '*', '*']},
         8: {'term': '고', 'pos': 'EC', 'feature': ['*', 'F', '고', '*', '*', '*', '*']},
         9: {'term': '있', 'pos': 'VX', 'feature': ['*', 'T', '있', '*', '*', '*', '*']}}
        """

        # API Info
        if api_host is None:
            self.api_host = self.HOST
        else:
            if api_host[:7] != "http://":
                api_host = "http://" + api_host
            elif api_host[:8] != "https://":
                api_host = "https://" + api_host
            if api_host[-1] == '/':
                api_host = api_host[:-1]
            self.api_host = api_host

        if api_port is None:
            self.api_port = self.PORT
        else:
            self.api_port = api_port

        if api_key is None:
            self.api_key = ""
        else:
            self.api_key = api_key

        # API Auth
        username = None
        password = None

        # DB Info
        if db_host is None:
            self.db_host = self.HOST
        else:
            self.db_host = db_host

        if db_port is None:
            self.db_port = self.PORT
        else:
            self.db_port = db_port

        # Text Bucket
        if bucket:
            self.bucket = bucket

    def __getattr__(self, name):
        """Get a database by name.

        :Parameters:
          - `name`: the name of the database to get
        """
        if name.startswith('_'):
            raise AttributeError(
                "TextClient has no attribute %r. To access the %s"
                " database, use tclient[%r]." % (name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a database by name.

        :Parameters:
          - `name`: the name of the database to get
        """
        return database.Database(self, name)
