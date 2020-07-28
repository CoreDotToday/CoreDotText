# -*- coding: utf-8 -*-
import requests
import json
import uuid
import logging
import re

from gensim import corpora, models
import scipy.io
import matplotlib.pylab as plt

__author__ = "Core.Today"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)
list_not_allowed_name =\
    [
        'bucket', 'tag', 'tagging', 'info',
        'list_database_names', 'drop', 'drop_database',
        'list_collection_names', 'tag_to_list',
        'tag_to_matrix', 'insert_one', 'delete_one',
        'update_one', 'make_dictionary', 'add_dictionary',
        'make_corpus', 'host', 'port',
        'api_host', 'api_port', 'db_host', 'db_port',
        'database_name', 'database_port', 'collection',
        'database', 'documents', 'custom', 'pos',
        'custom_pos', 'corpus', 'corpus_key',
        'documents', 'limit', 'pos', 'username', 'password'
    ]


class TextClient:
    HOST = "localhost"
    PORT = "80"

    def __init__(
            self,
            api_host=None,
            api_port=None,
            api_key=None,
            db_host=None,
            db_port=None,
            **kwargs):
        """tclient for NLP.

        The tclient object is .

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

        .. versionchanged:: 0.0.2
           Changed total structure to client, database, collection
        .. versionchanged:: 0.0.1
           the name ``text`` object

        Examples
        --------
        """
        self.database_type = 0  # 0: memory, 1: MongoDB
        self.database_name = None
        self.database = dict()

        # API Info
        if api_host is None:
            self.api_host = self.HOST
        else:
            # if api_host[:7] != "http://":
            #     api_host = "http://" + api_host
            # elif api_host[:8] != "https://":
            #     api_host = "https://" + api_host
            if api_host[-1] == '/':
                api_host = api_host[:-1]
            self.api_host = api_host

        if api_port is None:
            self.api_port = self.PORT
        else:
            self.api_port = str(api_port)

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

        if name in list_not_allowed_name:
            raise Exception("Try another name. This name is not allowed.")

        self.database_name = name
        if name not in self.database:
            self.database[name] = Database(self.info(), name)
        return self.database[name]

    def info(self):
        information = dict()
        information['api_host'] = self.api_host
        information['api_port'] = self.api_port
        information['api_key'] = self.api_key
        information['database_type'] = self.database_type
        information['version'] = __version__
        return information

    def list_database_names(self):
        return list(self.database.keys())

    def drop(self):
        self.database = dict()

    def drop_database(self, name):
        self.database.pop(name)


class Database:
    def __init__(self, info, name):
        self.api_host = info['api_host']
        self.api_port = info['api_port']
        self.api_key = info['api_key']
        self.database_type = info['database_type']
        self.database_name = name
        self.collection = dict()

    def __getattr__(self, name):
        """Get a collection by name.

        :Parameters:
          - `name`: the name of the collection to get
        """
        if name.startswith('_'):
            raise AttributeError(
                "Database has no attribute %r. To access the %s"
                " database, use database[%r]." % (name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a collection by name.

        :Parameters:
          - `name`: the name of the collection to get
        """
        if name in list_not_allowed_name:
            raise Exception("Try another name. This name is not allowed.")

        if type(name) != str:
            raise Exception("name must be string")

        self.collection_name = name
        if name not in self.collection:
            self.collection[name] = Collection(self.info())
        return self.collection[name]

    def bucket(self):
        raise Exception("Assign bucket in the collection")

    def info(self):
        information = dict()
        # TextClient
        information['api_host'] = self.api_host
        information['api_port'] = self.api_port
        information['api_key'] = self.api_key
        information['database_type'] = self.database_type
        information['version'] = __version__
        return information

    def list_collection_names(self):
        return list(self.collection.keys())


class Collection:

    def __init__(self, info):
        self.api_host = info['api_host']
        self.api_port = info['api_port']
        self.api_key = info['api_key']

        self.bucket = ""  # Text Bucket
        self.tag = dict()

        self.custom = list()  # custom_keywords
        self.custom_pos = list()  # custom_keywords_pos

        self.documents = dict()
        self.dictionary = None
        self.corpus = None
        self.corpus_key = None
        self.tfidf = None
        self.tfidf_model = None

        self.database_type = 0

    def info(self):
        information = dict()
        # TextClient
        information['api_host'] = self.api_host
        information['api_port'] = self.api_port
        information['api_key'] = self.api_key
        information['database_type'] = self.database_type
        # Database
        information['count_documents'] = len(self.documents)
        information['custom'] = self.custom
        information['custom_pos'] = self.custom_pos
        information['version'] = __version__
        return information

    def tagging(self, bucket="", data=None, custom=[], custom_pos=[], update=1):
        """
        Tagging(POS, Part Of Speech) of bucket

        :return: dict(tag)
        """

        # Choice target bucket
        if bucket:
            """
            Given bucket as a parameter
            """
            target_bucket = bucket
        elif self.bucket:
            """
            self.bucket
            """
            target_bucket = self.bucket
        # else:
        #     raise Exception('bucket is empty')

        # Choice custom
        if custom:
            if type(custom) == str:
                custom = [custom]
            target_custom = custom
        else:
            # elif self.custom:
            target_custom = self.custom

        if custom_pos:
            target_custom_pos = custom_pos
        else:
            target_custom_pos = self.custom_pos

        if target_custom:
            """
            replace custom keywords to temporary stone
            """
            temp_custom_id = dict()  # temporarily generated terms set
            for custom_key in target_custom:
                _id = get_unique_id_eng()
                target_bucket = target_bucket.replace(custom_key, _id+" ")  # 붙어 있는 term에 대한 구분을 위하여 " "를 붙임.
                temp_custom_id[_id] = custom_key
            # # temporarily
            # self.temp_custom_id = temp_custom_id

        if data:
            # already parsed data
            data = data
        else:
            if target_bucket:
                # r = requests.post(self.api_host+":"+self.api_port,
                r = requests.post(self.api_host,
                                  data={"text": target_bucket, "key": self.api_key})
                res = r.text
            else:
                raise Exception('bucket is empty')

            data = json.loads(res)

        # Parsing
        if 'tokens' in data:
            # Syntax
            pass

        elif 'entities' in data:
            # Entities
            result = dict()
            for idx, i in enumerate(sorted(data['entities'], key=lambda k: k['mentions'][0]['text']['beginOffset'])):
                temp = dict()
                temp['term'] = i['name']
                temp['pos'] = i['type']
                temp['salience'] = i['salience']
                if i['metadata']:
                    if 'wikipedia_url' in i['metadata']:
                        temp['feature'] = i['metadata']['wikipedia_url']
                result[idx] = temp
            return result

        else:
            # MeCab

            # Convert index to int type
            temp = dict()
            for key in data.keys():
                temp[int(key)] = data[key]

            # CUSTOM Keywords
            if target_custom:
                if target_custom_pos:
                    custom_zip = dict()
                    if type(target_custom_pos) == str:
                        for key in target_custom:
                            custom_zip[key] = target_custom_pos
                    else:
                        for key, value in zip(target_custom, target_custom_pos):
                            custom_zip[key] = value

                for idx in temp:
                    if temp[idx]['term'] in temp_custom_id:
                        ori_term = temp_custom_id[temp[idx]['term']]
                        temp[idx]['term'] = ori_term
                        if target_custom_pos:
                            temp[idx]['pos'] = custom_zip[ori_term]
                        else:
                            temp[idx]['pos'] = "CUSTOM"
                        temp[idx]['feature'] = ['*', '*', ori_term, '*', '*', '*', '*']

            # Save tag to self.tag
            # if update and bucket: # 왜 이렇게 만들었지? 20180801
            if update:
                self.tag = temp
                if bucket:
                    self.bucket = bucket

                return self.tag
            else:
                return temp

    def tag_to_list(self, bucket="", data=None, limit=None, pos=None, combine=[], combine_char='/', custom=[], custom_pos=[], update=0):
        """
        Convert dict(tag) to list(tag)

        :param bucket:
        :param limit: string or list
        :param pos:
        :param combine: ['term', 'pos']
        :param combine_char: 'term'+combine_char+'pos'
        :param update:
        :return: list of tag
        """

        # Choice tag
        if bucket:
            # bucket to tag to list
            target_tag = self.tagging(bucket=bucket, data=data, custom=custom, custom_pos=custom_pos, update=update)
        elif not self.tag:
            # Check the data of self.tag
            target_tag = self.tagging(custom=custom, data=data, custom_pos=custom_pos)
        else:
            target_tag = self.tag

        # Check the type of limit
        if type(limit) == str:
            limit = [limit]

        # Check the type of pos
        if type(pos) == str:
            pos = [pos]

        if type(combine) != list:
            raise Exception("combine must be list")

        if combine != list():
            limit = combine
            # if limit is None:
            #     limit = combine

        result = list()
        for index in range(len(target_tag)):
            # None, term, pos, feature
            if limit:
                # Temporary list
                temp = []

                for key in limit:
                    if pos:
                        if target_tag[index]['pos'] in pos:
                            temp.append(target_tag[index][key])
                    else:
                        temp.append(target_tag[index][key])

                if temp:
                    if combine:
                        temp_combine = ''
                        for combine_key in combine:
                            temp_combine += combine_char + str(temp[limit.index(combine_key)])
                        temp = temp_combine[len(combine_char):]

                    if len(temp) == 1:
                        # prevent empty list
                        result.append(temp[0])
                    else:
                        result.append(temp)

            else:
                if pos:
                    if target_tag[index]['pos'] in pos:
                        result.append(target_tag[index])
                else:
                    result.append(target_tag[index])

        return result

    def tag_to_matrix(self):
        """
        Convert dict(tag) to matrix(TF type)

        :return: np.matrix()
        """

        return None


    """
    CRUD
    """
    def insert_one(self, doc_name=None, bucket="", data=None, limit="term",
                   pos=None, custom=[], custom_pos=[], tag_list=[],
                   combine=[], combine_char='/'
                   ):
        """

        :param doc_name:
        :param bucket:
        :param limit:
        :param tag_list: choose bucket or tag_list
        :return:
        """

        # Set the document name
        if doc_name is None:
            doc_name = get_unique_id()

        # Set the document content
        if bucket == "" and tag_list == [] and data is None:
            raise Exception("bucket parameter is empty")

        # tag = self.tagging(bucket=bucket, update=0)
        if doc_name in self.documents:
            raise Exception("doc_name already exists")

        if tag_list:
            """
            tag_to_list와 같은 값을 API 없이 넣을 때
            [{'term': '안녕',
              'pos': 'NNG',
              'feature': ['행위', 'T', '안녕', '*', '*', '*', '*']},
             {'term': '하', 'pos': 'XSV', 'feature': ['*', 'F', '하', '*', '*', '*', '*']},
             {'term': '세요',
              'pos': 'EP+EF',
              'feature': ['*', 'F', '세요', 'Inflect', 'EP', 'EF', '시/EP/*+어요/EF/*']},
             {'term': '파이썬',
              'pos': 'NNP',
              'feature': ['*', 'T', '파이썬', '*', '*', '*', '*']},
             {'term': '을', 'pos': 'JKO', 'feature': ['*', 'T', '을', '*', '*', '*', '*']},
             {'term': '재밌', 'pos': 'VA', 'feature': ['*', 'T', '재밌', '*', '*', '*', '*']},
             {'term': '게', 'pos': 'EC', 'feature': ['*', 'F', '게', '*', '*', '*', '*']},
             {'term': '배우', 'pos': 'VV', 'feature': ['*', 'F', '배우', '*', '*', '*', '*']},
             {'term': '고', 'pos': 'EC', 'feature': ['*', 'F', '고', '*', '*', '*', '*']},
             {'term': '있', 'pos': 'VX', 'feature': ['*', 'T', '있', '*', '*', '*', '*']},
             {'term': '습니다',
              'pos': 'EF',
              'feature': ['*', 'F', '습니다', '*', '*', '*', '*']},
             {'term': '하하하',
              'pos': 'IC',
              'feature': ['*', 'F', '하하하', '*', '*', '*', '*']}]
            """
            if type(tag_list) != list:
                raise Exception("tag must be list")
            self.documents[doc_name] = tag_list

        else:
            self.documents[doc_name] = self.tag_to_list(
                bucket=bucket,
                data=data,
                limit=limit,
                pos=pos,
                custom=custom,
                custom_pos=custom_pos,
                combine=combine, combine_char=combine_char
            )

    def find_one(self, doc_name=None):
        if doc_name is None:
            raise Exception("doc_name missing")

        if doc_name not in self.documents:
            raise Exception("doc_name not exists")

        return self.documents[doc_name]

    def update_one(self, doc_name=None, bucket="", limit="term", pos=None, custom=[], custom_pos=[], tag_list=[]):
        if doc_name not in self.documents:
            raise Exception("doc_name not exists")

        if tag_list:
            if type(tag_list) != list():
                raise Exception("tag must be list")
            self.documents[doc_name] = tag_list

        else:
            self.documents[doc_name] = self.tag_to_list(
                bucket=bucket,
                limit=limit,
                pos=pos,
                custom=custom,
                custom_pos=custom_pos
            )

    def delete_one(self, doc_name=None):
        if doc_name not in self.documents:
            raise Exception("doc_name not exists")
        self.documents.pop(doc_name)

    def drop(self):
        if self.database_type == 0:
            # Memory
            self.documents = dict()
        elif self.database_type == 0:
            # MongoDB
            None

    """
    Dictionary
    """

    def make_dictionary(self):
        from gensim.corpora import Dictionary

        self.dictionary = Dictionary(self.documents.values())

        logger.info(
            "generated dictionary by Dictionary of gensim.corpora"
        )
        return self.dictionary

    def add_dictionary(self, vocab, prune_at=2000000):
        if not self.dictionary:
            raise Exception("self.dictionary is empty. First run make_dictionary")

        if type(vocab) != list:
            raise Exception("Type of vocab must be list")

        self.dictionary.add_documents([vocab], prune_at=prune_at)

        logger.info(
            "built %s from %i documents (total %i corpus positions)",
            self.dictionary, self.dictionary.num_docs, self.dictionary.num_pos
        )
        return self.dictionary

    # def doc2bow(self):
    #     self.tag_to_list()

    """
    Corpus
    """
    def make_corpus(self):
        if not self.dictionary:
            self.make_dictionary()

        doc_corpus = list()
        doc_key_set = list()
        for doc_key in self.documents:
            doc_key_set.append(doc_key)
            doc_corpus.append(self.dictionary.doc2bow(self.documents[doc_key]))

        self.corpus = doc_corpus
        self.corpus_key = doc_key_set
        return self.corpus_key, self.corpus

        # logger.info(
        #     "generated corpus"
        # )

    """
    TF-IDF
    
    Ref : https://radimrehurek.com/gensim/models/tfidfmodel.html
    """
    def make_tfidf_model(self, corpus=None):
        from gensim import models

        if not corpus:
            corpus = self.corpus

        tfidf_model = models.TfidfModel(corpus)
        self.tfidf_model = tfidf_model
        return self.tfidf_model

    def make_tfidf(self, corpus=None):
        if not corpus:
            corpus = self.corpus

        if not self.tfidf:
            self.make_tfidf_model()

        tfidf = self.tfidf_model[corpus]
        self.tfidf = tfidf
        return self.tfidf

    def draw_tfidf(self, mm_path='/tmp/corpus_temp.mm', tfidf=None, figsize=(10, 10)):
        # from gensim import corpora
        # import scipy.io
        # import matplotlib.pylab as plt

        if not tfidf:
            tfidf = self.tfidf

        corpora.MmCorpus.serialize(mm_path, tfidf.corpus)
        m = scipy.io.mmread(mm_path)

        plt.figure(figsize=figsize)
        return plt.imshow(m.todense().T, aspect='auto', vmin=0, vmax=2, cmap='Greys', interpolation='nearest')




"""
Common Functions
"""


def get_unique_id():
    """
    for unique random docname
    :return: length 32 string
    """
    _id = str(uuid.uuid4()).replace("-", "")
    return _id


def get_unique_id_eng(length=10):
    _id = str(uuid.uuid4()).replace("-", "")
    result = "".join(re.findall("[a-zA-Z]+", _id))
    result = result[:length]
    return result

